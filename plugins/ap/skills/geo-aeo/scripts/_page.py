"""_page.py — extract what a NON-rendering crawler sees in a page's raw HTML.

Most AI fetchers (GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot and the user-triggered
fetchers) read the server HTML and do not run JavaScript. So this parser deliberately
reads the raw response only: if a fact is not in here, assume those systems cannot see it.
Use render_diff.mjs to measure what JavaScript adds on top.
"""
from __future__ import annotations

import json
import re
import urllib.parse
from dataclasses import dataclass, field
from html.parser import HTMLParser

SKIP = {"script", "style", "template", "svg", "math", "iframe", "object", "canvas"}
CHROME = {"nav", "header", "footer", "aside", "form", "dialog"}
BLOCK = {"p", "div", "li", "td", "th", "section", "article", "main", "blockquote", "pre",
         "h1", "h2", "h3", "h4", "h5", "h6", "dd", "dt", "figcaption", "br", "tr", "summary"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
QUESTION_START = re.compile(
    r"^(what|why|how|when|where|who|which|whose|can|could|should|would|will|is|are|was|were|do|does|did|"
    r"has|have|may|apa|bagaimana|kenapa|mengapa|bila|di mana|siapa|berapa|boleh)\b",
    re.I,
)
WORD = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\u0e00-\u0e7f]|[\w'’-]+", re.U)
# Chinese/Japanese/Thai characters count one "word" each (no spaces between words); rough but it stops
# those pages reading as empty. Korean uses spaces, so \\w already handles it.
NUMBER = re.compile(r"(?<![\w.])(\d{1,3}(?:[,.]\d{3})+|\d+(?:\.\d+)?)\s?(%|percent|x\b|×)?", re.I)
DATE_TEXT = re.compile(
    r"\b(\d{4}-\d{2}-\d{2}|\d{1,2} (?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]* \d{4}|"
    r"(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]* \d{1,2},? \d{4})\b",
    re.I,
)
UPDATED_TEXT = re.compile(r"\b(updated|last updated|reviewed|last reviewed|dikemas kini)\b", re.I)


@dataclass
class Section:
    level: int
    heading: str
    first_para: str = ""
    words: int = 0
    lists: int = 0
    tables: int = 0
    lead: str = ""          # first ~80 words of section text, for div-soup pages without <p>


@dataclass
class Page:
    url: str
    lang: str = ""
    title: str = ""
    titles: int = 0
    meta: dict = field(default_factory=dict)          # name/property -> content (lowercase keys)
    canonical: list = field(default_factory=list)
    hreflang: list = field(default_factory=list)       # (lang, href)
    alternates: list = field(default_factory=list)     # (type, href) e.g. text/markdown, rss
    jsonld_raw: list = field(default_factory=list)
    jsonld: list = field(default_factory=list)         # parsed objects (flattened @graph)
    jsonld_errors: list = field(default_factory=list)
    microdata_types: list = field(default_factory=list)
    headings: list = field(default_factory=list)       # (level, text)
    sections: list = field(default_factory=list)
    words_total: int = 0
    words_content: int = 0                              # excluding nav/header/footer/aside
    words_main: int = 0                                 # inside <main>/<article>
    has_main: bool = False
    paragraphs: list = field(default_factory=list)
    lists: int = 0
    tables: int = 0
    images: int = 0
    images_no_alt: int = 0
    images_empty_alt: int = 0
    links_internal: list = field(default_factory=list)
    links_external: list = field(default_factory=list)
    nofollow_internal: int = 0
    time_tags: list = field(default_factory=list)
    script_bytes_inline: int = 0
    scripts_external: int = 0
    noscript_words: int = 0
    iframes: int = 0
    videos: int = 0
    details: int = 0
    html_bytes: int = 0
    text_sample: str = ""
    root_shell: bool = False
    author_hints: list = field(default_factory=list)
    forms: int = 0
    inputs_unlabelled: int = 0
    head_in_body: list = field(default_factory=list)   # head-only tags found after <body> started
    visible_text: str = ""                              # all rendered-as-text content, capped
    content_text: str = ""                              # main content (no nav/header/footer), capped
    letter_runs: int = 0                                # runs of >=5 consecutive 1-char text nodes
    contact_links: int = 0                              # mailto:, tel:, WhatsApp links
    email_obfuscated: bool = False                      # Cloudflare Email Obfuscation in use


class _P(HTMLParser):
    def __init__(self, page: Page):
        super().__init__(convert_charrefs=True)
        self.p = page
        self.skip = 0
        self.chrome = 0
        self.main = 0
        self.in_title = False
        self.head_level = 0
        self.head_buf: list[str] = []
        self.para_buf: list[str] | None = None
        self.in_jsonld = False
        self.jsonld_buf: list[str] = []
        self.in_script = False
        self.script_len = 0
        self.noscript = 0
        self.text_parts: list[str] = []
        self.content_parts: list[str] = []
        self.main_parts: list[str] = []
        self.cur_section: Section | None = None
        self.want_first_para = False
        self.link_stack: list = []
        self.labels_for: set = set()
        self.input_ids: list = []
        self.in_label = 0
        self.in_body = False
        self.char_run = 0

    # --- tags ---------------------------------------------------------------------------
    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        p = self.p
        if tag == "body":
            self.in_body = True
        if self.in_body and not self.skip and (tag == "title" or (tag == "link" and "canonical" in a.get("rel", "").lower())
                                               or (tag == "meta" and a.get("name", "").lower() in ("description", "robots"))):
            p.head_in_body.append(tag if tag != "meta" else "meta " + a.get("name", "").lower())
        if tag == "html":
            p.lang = a.get("lang", "")
        elif tag == "title" and not self.skip:
            self.in_title = True
            p.titles += 1
        elif tag == "meta":
            key = (a.get("name") or a.get("property") or a.get("http-equiv") or a.get("itemprop") or "").lower()
            if key:
                if key in p.meta and key in ("robots", "googlebot", "description"):
                    p.meta[key] += " | " + a.get("content", "")
                else:
                    p.meta[key] = a.get("content", "")
        elif tag == "link":
            rel = a.get("rel", "").lower().split()
            href = a.get("href", "")
            if "canonical" in rel:
                p.canonical.append(href)
            if "alternate" in rel:
                if a.get("hreflang"):
                    p.hreflang.append((a["hreflang"], href))
                elif a.get("type"):
                    p.alternates.append((a["type"], href))
            if "author" in rel:
                p.author_hints.append(f"link rel=author {href}")
        elif tag == "script":
            t = a.get("type", "").lower()
            if "ld+json" in t:
                self.in_jsonld = True
                self.jsonld_buf = []
            else:
                self.in_script = True
                self.script_len = 0
                if a.get("src"):
                    p.scripts_external += 1
            self.skip += 1
            return
        if tag in SKIP and tag != "script":
            self.skip += 1
            if tag == "iframe":
                p.iframes += 1
            return
        if tag == "noscript":
            self.noscript += 1
        if a.get("itemtype"):
            p.microdata_types.append(a["itemtype"].rstrip("/").split("/")[-1])
        if "author" in (a.get("class", "") + " " + a.get("rel", "") + " " + a.get("itemprop", "")).lower():
            p.author_hints.append(f"<{tag} class/itemprop mentions author>")
        if tag in CHROME:
            self.chrome += 1
        if tag in ("main", "article"):
            self.main += 1
            p.has_main = True
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._flush_para()
            self.head_level = int(tag[1])
            self.head_buf = []
        elif tag == "p":
            self._flush_para()
            self.para_buf = []
        elif tag in ("div", "section", "article", "main", "ul", "ol", "table", "blockquote", "pre", "figure", "form"):
            self._flush_para()  # these implicitly close an open <p>
        if tag in ("ul", "ol"):
            p.lists += 1
            if self.cur_section:
                self.cur_section.lists += 1
        elif tag == "table":
            p.tables += 1
            if self.cur_section:
                self.cur_section.tables += 1
        elif tag == "img":
            p.images += 1
            if "alt" not in a:
                p.images_no_alt += 1
            elif not a["alt"].strip():
                p.images_empty_alt += 1
        elif tag == "a":
            href = a.get("href", "")
            rel = a.get("rel", "").lower()
            self.link_stack.append([href, rel, []])
        elif tag == "time":
            p.time_tags.append(a.get("datetime", ""))
        elif tag == "video":
            p.videos += 1
        elif tag == "details":
            p.details += 1
        elif tag == "form":
            p.forms += 1
        elif tag == "label":
            self.in_label += 1
            if a.get("for"):
                self.labels_for.add(a["for"])
        elif tag in ("input", "select", "textarea"):
            if a.get("type", "").lower() not in ("hidden", "submit", "button", "image", "reset"):
                labelled = bool(a.get("aria-label") or a.get("aria-labelledby") or a.get("title") or self.in_label)
                self.input_ids.append((a.get("id", ""), labelled))
        if tag in BLOCK or tag == "br":
            self._txt(" \n ")

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        p = self.p
        if tag == "script":
            if self.in_jsonld:
                raw = "".join(self.jsonld_buf).strip()
                p.jsonld_raw.append(raw)
                self.in_jsonld = False
            elif self.in_script:
                p.script_bytes_inline += self.script_len
                self.in_script = False
            self.skip = max(0, self.skip - 1)
            return
        if tag in SKIP:
            self.skip = max(0, self.skip - 1)
            return
        if tag == "title":
            self.in_title = False
        elif tag == "noscript":
            self.noscript = max(0, self.noscript - 1)
        elif tag in CHROME:
            self.chrome = max(0, self.chrome - 1)
        elif tag in ("main", "article"):
            self.main = max(0, self.main - 1)
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6") and self.head_level:
            text = _clean(" ".join(self.head_buf))
            p.headings.append((self.head_level, text))
            if self.head_level >= 2 and not self.chrome:
                self.cur_section = Section(self.head_level, text)
                p.sections.append(self.cur_section)
                self.want_first_para = True
            self.head_level = 0
        elif tag == "p":
            self._flush_para()
        elif tag == "a" and self.link_stack:
            href, rel, txt = self.link_stack.pop()
            self._record_link(href, rel, _clean(" ".join(txt)))
        elif tag == "label":
            self.in_label = max(0, self.in_label - 1)
        if tag in BLOCK:
            self._txt(" \n ")

    def handle_data(self, data):
        if self.in_jsonld:
            self.jsonld_buf.append(data)
            return
        if self.in_script:
            self.script_len += len(data)
            return
        if self.skip:
            return
        if self.in_title:
            self.p.title += data
            return
        if self.head_level:
            self.head_buf.append(data)
        if self.para_buf is not None:
            self.para_buf.append(data)
        for l in self.link_stack:
            l[2].append(data)
        t = data.strip()
        if t:
            if len(t) == 1:
                self.char_run += 1
            else:
                if self.char_run >= 5:
                    self.p.letter_runs += 1
                self.char_run = 0
        self._txt(data)

    # --- helpers ------------------------------------------------------------------------
    def _txt(self, data):
        self.text_parts.append(data)
        if self.noscript:
            self.p.noscript_words += len(WORD.findall(data))
        if not self.chrome:
            self.content_parts.append(data)
            if self.cur_section and data.strip():
                self.cur_section.words += len(WORD.findall(data))
                if self.cur_section.words <= 90:
                    self.cur_section.lead += " " + data
        if self.main:
            self.main_parts.append(data)

    def _flush_para(self):
        if self.para_buf is None:
            return
        text = _clean(" ".join(self.para_buf))
        self.para_buf = None
        if not text:
            return
        if not self.chrome:
            self.p.paragraphs.append(text)
            if self.want_first_para and self.cur_section and len(WORD.findall(text)) >= 4:
                self.cur_section.first_para = text
                self.want_first_para = False

    def _record_link(self, href, rel, text):
        low = (href or "").lower()
        if low.startswith(("mailto:", "tel:")) or "wa.me/" in low or "api.whatsapp.com" in low or "whatsapp://" in low:
            self.p.contact_links += 1
        if "/cdn-cgi/l/email-protection" in low:
            self.p.email_obfuscated = True
            self.p.contact_links += 1
            return
        if not href or href.startswith(("#", "javascript:", "mailto:", "tel:", "data:")) or "/cdn-cgi/" in href:
            return
        absu = urllib.parse.urljoin(self.p.url, href)
        host = urllib.parse.urlsplit(absu).hostname or ""
        base = urllib.parse.urlsplit(self.p.url).hostname or ""
        strip = lambda h: h[4:] if h.startswith("www.") else h  # noqa: E731
        if strip(host) == strip(base):
            self.p.links_internal.append((absu.split("#")[0], text))
            if "nofollow" in rel:
                self.p.nofollow_internal += 1
        else:
            self.p.links_external.append((absu, text, rel))

    def finish(self):
        self._flush_para()
        p = self.p
        p.title = _clean(p.title)
        all_text = _clean(" ".join(self.text_parts))
        p.words_total = len(WORD.findall(all_text))
        p.words_content = len(WORD.findall(" ".join(self.content_parts)))
        p.words_main = len(WORD.findall(" ".join(self.main_parts)))
        p.text_sample = _clean(" ".join(self.content_parts))[:600]
        p.visible_text = all_text[:300_000]
        p.content_text = _clean(" ".join(self.content_parts))[:200_000]
        if self.char_run >= 5:
            p.letter_runs += 1
        for sec in p.sections:
            sec.lead = _clean(sec.lead)
            if not sec.first_para and sec.lead:
                sec.first_para = sec.lead
        for i, (iid, labelled) in enumerate(self.input_ids):
            if not labelled and not (iid and iid in self.labels_for):
                p.inputs_unlabelled += 1


def _clean(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


def _flatten(obj, out: list):
    if isinstance(obj, list):
        for o in obj:
            _flatten(o, out)
    elif isinstance(obj, dict):
        if "@graph" in obj and isinstance(obj["@graph"], list):
            ctx = obj.get("@context")
            for o in obj["@graph"]:
                if isinstance(o, dict) and ctx and "@context" not in o:
                    o = {**o, "@context": ctx}
                _flatten(o, out)
        else:
            out.append(obj)


def parse_page(url: str, html: str) -> Page:
    page = Page(url=url, html_bytes=len(html.encode("utf-8", errors="ignore")))
    parser = _P(page)
    try:
        parser.feed(html)
        parser.close()
    except Exception:
        pass
    parser.finish()
    if "email-decode.min.js" in html or "__cf_email__" in html:
        page.email_obfuscated = True
    for raw in page.jsonld_raw:
        if not raw:
            page.jsonld_errors.append("empty ld+json block")
            continue
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            # Common real-world breakage: trailing commas, HTML comments, unescaped newlines.
            try:
                data = json.loads(re.sub(r",\s*([}\]])", r"\1", raw.replace("<!--", "").replace("-->", "")))
                page.jsonld_errors.append(f"invalid JSON (recoverable, strict parsers will reject it): {e}")
            except Exception:
                page.jsonld_errors.append(f"invalid JSON: {e}")
                continue
        _flatten(data, page.jsonld)
    # SPA shell: almost no text but an app root and heavy scripts.
    # SPA shell: almost no text at all, no h1, and an app mount point. Thin-but-rendered pages
    # (sparse listings) are a content finding, not a rendering one.
    has_root = re.search(r'id=["\'](root|app|__next|__nuxt|svelte|q-app|___gatsby)["\']', html)
    if has_root and (page.words_total < 50 or (page.words_content < 25 and not any(l == 1 for l, _ in page.headings))):
        page.root_shell = True
    return page


def types_of(obj: dict) -> list[str]:
    t = obj.get("@type", [])
    if isinstance(t, str):
        t = [t]
    return [str(x).split("/")[-1].split(":")[-1] for x in t]


def all_types(objs, depth: int = 0) -> list[str]:
    """Every @type in the JSON-LD, including nested ones (Offer inside Product, etc.)."""
    out: list[str] = []
    if depth > 8:
        return out
    if isinstance(objs, dict):
        if "@type" in objs:
            out += types_of(objs)
        for k, v in objs.items():
            if not k.startswith("@") or k == "@graph":
                out += all_types(v, depth + 1)
    elif isinstance(objs, list):
        for v in objs:
            out += all_types(v, depth + 1)
    return out


def is_question(h: str) -> bool:
    h = h.strip()
    return h.endswith("?") or bool(QUESTION_START.match(h))


def count_numbers(text: str) -> int:
    return len(NUMBER.findall(text))


def words(text: str) -> int:
    return len(WORD.findall(text))
