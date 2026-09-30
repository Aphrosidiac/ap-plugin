"""_robots.py — RFC 9309 robots.txt evaluation, the way Google and the major AI crawlers read it.

Why not urllib.robotparser: it applies rules first-match instead of longest-match, ignores
`*` / `$` wildcards, and does not merge repeated groups — so it gives wrong answers on exactly
the files that matter (the ones with specific Allow carve-outs under a broad Disallow).

Rules implemented:
- A crawler obeys ONE group: the one whose user-agent token equals its product token
  (case-insensitive; "GPTBot/1.1" is read as "gptbot"). Several groups naming the same token
  are merged. If none match, the `*` group applies. If there is no `*` group, all is allowed.
- Consecutive `User-agent:` lines share the rules that follow them.
- Within the group, the longest matching path pattern wins; on a tie, Allow wins.
- `*` matches any run of characters; `$` anchors the end. An empty `Disallow:` allows all.
- Non-standard lines (Crawl-delay, Content-Signal, Host, Clean-param) are collected, not applied.
"""
from __future__ import annotations

import re
import urllib.parse
from dataclasses import dataclass, field


@dataclass
class Group:
    agents: list = field(default_factory=list)
    rules: list = field(default_factory=list)  # (allow: bool, pattern: str)
    extras: dict = field(default_factory=dict)  # lowercase key -> [values]


@dataclass
class Robots:
    groups: list
    sitemaps: list
    extras: dict  # file-level non-standard lines
    raw: str
    errors: list

    def group_for(self, token: str, fallback: str | None = None) -> Group | None:
        t = token.lower()
        hits = [g for g in self.groups if t in g.agents]
        if not hits and fallback:
            # e.g. Applebot obeys the Googlebot group when it is not named itself.
            hits = [g for g in self.groups if fallback.lower() in g.agents]
        if not hits:
            hits = [g for g in self.groups if "*" in g.agents]
        if not hits:
            return None
        merged = Group(agents=[t])
        for g in hits:
            merged.rules.extend(g.rules)
            for k, v in g.extras.items():
                merged.extras.setdefault(k, []).extend(v)
        return merged

    def names_token(self, token: str) -> bool:
        return token.lower() in {a for g in self.groups for a in g.agents}

    def allowed(self, token: str, url_or_path: str, fallback: str | None = None) -> tuple[bool, str]:
        """Return (allowed, deciding_rule). deciding_rule is '' when nothing matched."""
        path = _path_of(url_or_path)
        g = self.group_for(token, fallback)
        if g is None:
            return True, ""
        best = None  # (len, allow, rule_text)
        for allow, pat in g.rules:
            if pat == "":
                continue  # "Disallow:" with no value = no restriction
            if _match(pat, path):
                cand = (len(pat), allow, f"{'Allow' if allow else 'Disallow'}: {pat}")
                if best is None or cand[0] > best[0] or (cand[0] == best[0] and allow and not best[1]):
                    best = cand
        if best is None:
            return True, ""
        return best[1], best[2]


def _path_of(u: str) -> str:
    if u.startswith("http://") or u.startswith("https://"):
        p = urllib.parse.urlsplit(u)
        path = p.path or "/"
        return path + (("?" + p.query) if p.query else "")
    return u or "/"


_pat_cache: dict = {}


def _match(pattern: str, path: str) -> bool:
    rx = _pat_cache.get(pattern)
    if rx is None:
        anchored = pattern.endswith("$")
        body = pattern[:-1] if anchored else pattern
        parts = [re.escape(p) for p in body.split("*")]
        rx = re.compile("^" + ".*".join(parts) + ("$" if anchored else ""))
        _pat_cache[pattern] = rx
    # Compare percent-decoded forms too, so /caf%C3%A9 and /café match either way.
    return bool(rx.match(path) or rx.match(urllib.parse.unquote(path)))


def parse(text: str) -> Robots:
    groups: list[Group] = []
    sitemaps: list[str] = []
    extras: dict = {}
    errors: list[str] = []
    cur: Group | None = None
    last_was_agent = False
    if text.startswith("﻿"):
        text = text[1:]
    for n, line in enumerate(text.splitlines(), 1):
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        if ":" not in line:
            errors.append(f"line {n}: no colon: {line[:60]}")
            continue
        key, val = line.split(":", 1)
        key = key.strip().lower()
        val = val.strip()
        if key in ("user-agent", "useragent", "user agent"):
            token = val.split("/")[0].strip().lower()
            if cur is not None and last_was_agent:
                cur.agents.append(token)
            else:
                cur = Group(agents=[token])
                groups.append(cur)
            last_was_agent = True
            continue
        last_was_agent = False
        if key == "sitemap":
            sitemaps.append(val)
            continue
        if key in ("allow", "disallow"):
            if cur is None:
                errors.append(f"line {n}: {key} before any User-agent")
                continue
            cur.rules.append((key == "allow", val))
            continue
        # Non-standard: Crawl-delay, Content-Signal, Host, Clean-param, Request-rate, ...
        target = cur.extras if cur is not None else extras
        target.setdefault(key, []).append(val)
        if key not in ("crawl-delay", "content-signal", "host", "clean-param", "request-rate", "visit-time", "noindex"):
            errors.append(f"line {n}: unknown directive '{key}'")
        if key == "noindex":
            errors.append(f"line {n}: 'Noindex' in robots.txt is unsupported by Google since 2019")
    return Robots(groups, sitemaps, extras, text, errors)
