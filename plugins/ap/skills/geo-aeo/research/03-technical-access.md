# 03 — Technical access for AI crawlers and agents (dossier, 2026-09-26)

Scope: everything an AI system needs to **fetch, render, parse and trust** a site: user agents, robots.txt, CDN/WAF behaviour, JS rendering, llms.txt and markdown, agent standards, sitemaps/feeds, and log verification.

Conventions: every claim carries `[source, date]`. "Fetched 2026-09-26" means the page was read during this research. **UNVERIFIED** marks claims that come only from secondary sources or could not be confirmed against a primary document.

---

## 0. The ten rules an agent should apply (TL;DR)

1. **AI answer engines only see what is in the raw HTML** unless the engine is Google (Gemini/AI Overviews use Googlebot's renderer) or Apple (Applebot renders). GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot and PerplexityBot were measured **not executing JS** [Vercel, 2024-12-17]. Server-render or prerender every piece of content you want cited.
2. **Treat training and retrieval as separate decisions.** Each vendor now has separate tokens: training (GPTBot, ClaudeBot, Google-Extended, Applebot-Extended, Meta-ExternalAgent, CCBot, MistralAI-Training, Amazonbot), search/index (OAI-SearchBot, Claude-SearchBot, PerplexityBot, Amzn-SearchBot, MistralAI-Index, Meta-WebIndexer, DuckAssistBot), and user-triggered fetchers (ChatGPT-User, Claude-User, Perplexity-User, Google-Agent, MistralAI-User, Meta-ExternalFetcher, Amzn-User).
3. **Blocking Google-Extended does NOT remove you from AI Overviews/AI Mode.** Those features use the normal Search index. To limit them you use `nosnippet`, `data-nosnippet`, `max-snippet`, or `noindex` [Google AI features doc, updated 2025-12-10].
4. **Microsoft has no AI robots.txt token.** Bing/Copilot grounding is controlled by `noarchive`/`nocache` meta tags, not robots.txt (secondary sources; Bing's help pages are JS-rendered and could not be fetched: UNVERIFIED against primary).
5. **Most user-triggered fetchers ignore robots.txt**: Google user-triggered fetchers (incl. Google-Agent), ChatGPT-User ("may not apply"), Perplexity-User, Meta-ExternalFetcher. Anthropic's Claude-User and MistralAI-User say they honour it.
6. **The CDN is the most common silent blocker.** Cloudflare has blocked AI crawlers by default for new domains since 2025-07-01. On 2026-09-15 it moved new domains to "Training + Agent blocked on pages with ads, Search allowed". Its "block Training" setting also blocks multi-purpose crawlers such as **Googlebot, Applebot and Bingbot** [Cloudflare blog, 2026-07-01]. Test with real UAs (see §6).
7. **llms.txt is optional and low-evidence.** Google says Search ignores it [Google AI optimization guide, 2026]. Ahrefs found 97% of llms.txt files got zero requests in May 2026 [Ahrefs, 2026-06-15]. Ship it cheaply if you like, but don't expect citations from it.
8. **Markdown via `Accept: text/markdown` is actually requested** by Claude's infrastructure and by agent tooling [suganthan.com log study, Mar–Apr 2026]. Cloudflare (Pro+) and Next.js on Vercel both support it. It's cheap, and it helps agents more than llms.txt.
9. **Verify bots by IP/rDNS/signature, never by UA alone.** Every major vendor publishes JSON IP ranges. Agents increasingly sign requests with Web Bot Auth (RFC 9421), which became an IETF WG Standards Track document on 2026-09-01 (secondary source).
10. **Serve clean 200s fast, with accurate `lastmod`, real 404/301s, and no interstitials** (cookie walls, bot challenges, geo-blocks) for the fetchers you want. AI crawlers waste about 35% of fetches on 404s and about 14% on redirects [Vercel, 2024-12-17].

---

## 1. Master user-agent table (state as of 2026-09-26)

Legend: **T** = training corpus, **S** = search/answer index, **U** = user-triggered live fetch, **Tok** = robots.txt token only (never appears in logs). robots column: Yes = documented as obeying; Partial = obeys for some purposes or per secondary reports; No = documented as generally ignoring.

| UA token | Owner | Type | robots.txt | Verify (IP list / rDNS) | Official doc |
|---|---|---|---|---|---|
| `GPTBot` (UA `...compatible; GPTBot/1.4; +https://openai.com/gptbot`) | OpenAI | T | Yes | https://openai.com/gptbot.json | developers.openai.com/api/docs/bots (fetched 2026-09-26) |
| `OAI-SearchBot` (UA `Mozilla/5.0 (Macintosh...) Chrome/131... ; compatible; OAI-SearchBot/1.4; +https://openai.com/searchbot`) | OpenAI | S (ChatGPT search) | Yes (~24 h to take effect) | https://openai.com/searchbot.json | same |
| `ChatGPT-User` (`...ChatGPT-User/1.0; +https://openai.com/bot`) | OpenAI | U (user actions, Custom GPTs, GPT Actions) | "robots.txt rules may not apply" (changed 2025-12-09) | https://openai.com/chatgpt-user.json | same; ppc.land 2025-12 |
| `OAI-AdsBot` (`...OAI-AdsBot/1.0; +https://openai.com/adsbot`) | OpenAI | Ad landing-page safety check; only pages submitted as ads; not training | n/a | https://openai.com/adsbot.json | same |
| ChatGPT agent / Atlas agent mode | OpenAI | U (browser agent) | Generic Chrome UA. Identify by `Signature-Agent: "https://chatgpt.com"` | keys at https://chatgpt.com/.well-known/http-message-signatures-directory | simonwillison.net 2025-08-04 |
| `ClaudeBot` | Anthropic | T | Yes, plus `Crawl-delay` | https://claude.com/crawling/bots.json | support.claude.com art. 8896518 (fetched 2026-09-26) |
| `Claude-SearchBot` | Anthropic | S | Yes, plus Crawl-delay | same list | same |
| `Claude-User` | Anthropic | U | Yes (honours robots.txt) | same list | same |
| `anthropic-ai`, `Claude-Web` | Anthropic | legacy tokens | Keep in block lists for old-UA safety | — | ai-robots-txt list (fetched 2026-09-26) |
| `Googlebot` | Google | S (Search, incl. AI Overviews / AI Mode grounding) | Yes | rDNS `*.googlebot.com`/`google.com`; `https://developers.google.com/static/crawling/ipranges/common-crawlers.json` (legacy `.../static/search/apis/ipranges/googlebot.json` still 200) | developers.google.com/.../google-common-crawlers |
| `Google-Extended` | Google | Tok: Gemini training + grounding use in Gemini apps/Vertex. "Does not impact a site's inclusion in Google Search nor is it used as a ranking signal" | Yes | n/a (no requests) | same |
| `Google-CloudVertexBot` | Google | Crawls "requested by site owners" for Vertex AI Agents | Yes | common-crawlers.json | same |
| `GoogleOther` (`-Image`, `-Video`) | Google | Generic R&D fetches | Yes | common-crawlers.json | same |
| `Google-Agent` | Google | U: "agents hosted on Google infrastructure to navigate the web and perform actions upon user request"; experimenting with Web Bot Auth (identity `https://agent.bot.auth`) | **No** ("generally ignore robots.txt") | `user-triggered-agents.json` | .../google-user-triggered-fetchers (updated 2026-08-19) |
| `Google-GeminiNotebook` (was `Google-NotebookLM`) | Google | U: fetches URLs users add as sources | No | user-triggered-fetchers*.json | same |
| `Google-Read-Aloud`, `FeedFetcher-Google` | Google | U / feeds | No | same | same |
| `bingbot` | Microsoft | S + Copilot grounding (no separate AI UA) | Yes; AI use via `noarchive`/`nocache` meta | https://www.bing.com/toolbox/bingbot.json; rDNS `*.search.msn.com` (rDNS: knowledge, UNVERIFIED this session) | bing.com/webmasters (JS page; secondary: better-robots.com, SEL 2023) |
| `PerplexityBot` | Perplexity | S; "not used to crawl content for AI foundation models" | Documented Yes; Cloudflare observed stealth evasion 2025-08-04 | https://www.perplexity.com/perplexitybot.json | docs.perplexity.ai/guides/bots |
| `Perplexity-User` | Perplexity | U | "generally ignores robots.txt" | https://www.perplexity.com/perplexity-user.json | same |
| `Applebot` | Apple | S (Siri/Spotlight/Safari) **and** T source | Yes; falls back to Googlebot rules if Applebot not named | rDNS `*.applebot.apple.com`; https://search.developer.apple.com/applebot.json | support.apple.com/en-us/119829 |
| `Applebot-Extended` | Apple | Tok: foundation-model training | Yes; blocking it keeps Search inclusion | n/a | same |
| `meta-externalagent` | Meta | T ("training foundation AI models or improving products by indexing content directly") | Yes (24 h) | no IP list (secondary) | developers.facebook.com/docs/sharing/webmasters/web-crawlers |
| `meta-webindexer` | Meta | S (Meta AI search quality) | Yes | — | same |
| `meta-externalfetcher` | Meta | U | "may bypass robots.txt" | — | same |
| `facebookexternalhit` | Meta | Link previews | May bypass for security checks | — | same |
| `Amazonbot` | Amazon | T + products; honours `noarchive` = no training | Yes (caches robots up to 30 days) | developer.amazon.com/amazonbot/ip-addresses/ | developer.amazon.com/amazonbot |
| `Amzn-SearchBot` | Amazon | S (Alexa/Rufus search); not training | Yes; follows other search-bot rules if not named | .../searchbot-ip-addresses/ | same |
| `Amzn-User` | Amazon | U (Alexa live answers); not training | Yes | .../live-ip-addresses/ | same |
| `DuckAssistBot` (`DuckAssistBot/1.2`) | DuckDuckGo | S/U for DuckAssist answers; "not used in any way to train AI models" | Yes (72 h) | https://duckduckgo.com/duckassistbot.json | duckduckgo.com/duckduckgo-help-pages/results/duckassistbot |
| `CCBot` (`CCBot/2.0`) | Common Crawl | T (upstream of most open LLM datasets) | Yes | https://index.commoncrawl.org/ccbot.json; rDNS `*.crawl.commoncrawl.org` | commoncrawl.org/ccbot |
| `MistralAI-User` | Mistral | U (Le Chat/Vibe) | Yes | https://mistral.ai/mistralai-user-ips.json | docs.mistral.ai/robots (fetched 2026-09-26) |
| `MistralAI-Index` | Mistral | S; not training | Yes | mistral.ai/mistralai-index-ips.json | same |
| `MistralAI-Training` | Mistral | T | Yes | — | same |
| `Bytespider`, `TikTokSpider`, `DoubaoBot` | ByteDance | T / unclear | Reported to ignore robots.txt and spoof UA (secondary) | none | UNVERIFIED (no official doc found) |
| `cohere-ai`, `cohere-training-data-crawler` | Cohere | T | UNVERIFIED | — | listed in ai-robots-txt |
| `DeepSeekBot` | DeepSeek | UNVERIFIED | UNVERIFIED | — | listed in ai-robots-txt; no official doc found |
| `GrokBot` / xAI | xAI | No official crawler docs. Reports of generic-browser UAs from proxies | No contract | none | nohacks.co 2026-08-08; secondary only (UNVERIFIED) |
| Others seen in 2026 block lists | various | `Claude-Code`, `Google-Gemini-CLI`, `Gemini-Deep-Research`, `GoogleAgent-Mariner`, `GoogleAgent-URLContext`, `Kimi-*`, `QwenBot`, `PanguBot`, `YouBot`, `Diffbot`, `ExaBot`, `TavilyBot`, `FirecrawlAgent`, `PetalBot`, `Timpibot`, `AzureAI-SearchBot`, `bedrockbot`, `Cloudflare-AutoRAG`, `NovaAct`, `Manus-User`, `Devin`, `Cursor` | varies | — | github.com/ai-robots-txt/ai.robots.txt robots.txt (fetched 2026-09-26) |

All IP-list URLs above returned HTTP 200 on 2026-09-26 (checked with curl). Each uses the Google-style `{"creationTime":..., "prefixes":[{"ipv4Prefix":...}|{"ipv6Prefix":...}]}` shape, except Common Crawl, which adds `synctoken`/`notes`.

Scale context: Googlebot reaches 1.70× more unique URLs than ClaudeBot, 1.76× more than GPTBot, 3.26× more than Bingbot, and 167× more than PerplexityBot (nohacks.co citing Cloudflare Jan-2026 data, 2026-08-08, secondary). Crawl-to-referral ratios: Google about 14:1, Anthropic about 73,000:1 in June 2025 [Cloudflare, 2025-07-01].

---

## 2. robots.txt semantics that trip people up

Primary reference: Google robots.txt spec (fetched 2026-09-26) and RFC 9309.

- **One group per crawler.** A crawler obeys only the group with the *most specific* matching UA. Groups naming the same UA are merged. Consequence: if you add `User-agent: GPTBot` with a single rule, GPTBot **stops obeying** everything under `User-agent: *`. Repeat any shared disallows (e.g. `/admin/`) inside each named group.
- **Longest path wins. On ties Google uses the least restrictive rule** (Allow beats Disallow).
- Wildcards: `*` = zero or more characters, `$` = end of URL. There's no regex.
- **Size limit 500 KiB.** Content past it is ignored. Google caches robots.txt up to 24 h.
- **HTTP status of robots.txt matters.** 4xx (except 429) = "no restrictions". 5xx = Google stops crawling for 12 h, then uses its cached copy for up to 30 days. **If your WAF 403s AI bots on /robots.txt, well-behaved bots treat it as "allow all" but then get 403 on pages.** Serve robots.txt as 200 `text/plain` to everyone.
- `Crawl-delay` is ignored by Google but honoured by Anthropic's bots [Anthropic support].
- robots.txt is per host and protocol. Each subdomain needs its own (Anthropic explicitly says so).
- Applebot falls back to Googlebot rules if Applebot isn't named [Apple]. Amzn-SearchBot falls back to the rules for "other search bots" [Amazon].
- Opt-out tokens (`Google-Extended`, `Applebot-Extended`) never appear in access logs. Don't try to verify them in logs.
- Change latency: OpenAI search ~24 h; Meta 24 h; DuckDuckGo 72 h; Amazon caches up to 30 days.
- robots.txt blocks **crawling**, not indexing of URLs discovered via links. To remove from Google's index or AI features, use `noindex` (and the page must be crawlable for Google to see it).

### 2.1 Page-level controls that matter for AI surfaces

```html
<!-- Google: keep out of AI Overviews/AI Mode snippets while staying indexed -->
<meta name="robots" content="max-snippet:0">         <!-- or nosnippet -->
<p>Public intro… <span data-nosnippet>text never to be quoted</span></p>

<!-- Bing/Copilot (secondary sources; UNVERIFIED on bing.com): -->
<meta name="robots" content="noarchive">  <!-- not used in Copilot answers / not for training (Bing, Amazonbot) -->
<meta name="robots" content="nocache">    <!-- Copilot may use only URL, title, snippet -->
```

HTTP header equivalent for non-HTML (PDFs etc.): `X-Robots-Tag: noarchive, max-snippet:0`.
Source: Google AI features doc (updated 2025-12-10) lists `nosnippet`, `data-nosnippet`, `max-snippet`, `noindex` as the AI-feature controls. Amazon honours `noarchive` = "do not use the page for model training" [developer.amazon.com/amazonbot]. Bing noarchive/nocache semantics: better-robots.com (2026) and Search Engine Land (Sept 2023, "Microsoft adds controls to disallow content in Bing Chat"), both secondary.

**GEO warning:** `nosnippet`, `max-snippet:0` and `noarchive` *reduce* AI citation eligibility. For a "maximize visibility" site, make sure none of them are set by accident (CMS defaults, SEO plugins, staging leftovers).

---

## 3. robots.txt templates

### Template A — Maximize AI search and answer visibility (allow everything, including training)

```txt
# robots.txt — maximize visibility in classic + AI search
User-agent: *
Allow: /
Disallow: /admin/
Disallow: /cart/
Disallow: /checkout/
Disallow: /account/
Disallow: /*?sessionid=
Disallow: /search?        # internal search results pages

# Optional AI-preference declaration (Cloudflare Content Signals syntax)
Content-Signal: search=yes, ai-input=yes, ai-train=yes

Sitemap: https://www.example.com/sitemap.xml
```

With no named groups, every bot inherits the `*` group. Only add named groups if you need different rules, and then **copy the shared Disallows into each named group**.

### Template B — Allow search and AI answers, refuse training (most common "GEO-safe" stance)

```txt
# 1) Default: everyone may crawl public pages
User-agent: *
Allow: /
Disallow: /admin/
Disallow: /account/
Content-Signal: search=yes, ai-input=yes, ai-train=no

# 2) Training-only crawlers and opt-out tokens: refuse
User-agent: GPTBot
User-agent: ClaudeBot
User-agent: anthropic-ai
User-agent: Google-Extended
User-agent: Applebot-Extended
User-agent: meta-externalagent
User-agent: CCBot
User-agent: MistralAI-Training
User-agent: Bytespider
User-agent: cohere-training-data-crawler
Disallow: /

# 3) Retrieval / answer engines: explicitly allowed (repeat shared rules!)
User-agent: OAI-SearchBot
User-agent: ChatGPT-User
User-agent: Claude-SearchBot
User-agent: Claude-User
User-agent: PerplexityBot
User-agent: Perplexity-User
User-agent: Amzn-SearchBot
User-agent: MistralAI-Index
User-agent: MistralAI-User
User-agent: DuckAssistBot
User-agent: meta-webindexer
Allow: /
Disallow: /admin/
Disallow: /account/

Sitemap: https://www.example.com/sitemap.xml
```

Notes:
- Consecutive `User-agent:` lines form one group (RFC 9309).
- **Do not** put `Googlebot`, `bingbot` or `Applebot` in the training block. Blocking them kills classic search *and* AI Overviews/Copilot/Siri. Use `Google-Extended`/`Applebot-Extended` for training opt-out and `noarchive` for Bing.
- `Amazonbot` is dual-purpose (training + product features). Decide deliberately. Blocking it may affect Alexa answers, while `Amzn-SearchBot` stays allowed.
- `ChatGPT-User`, `Perplexity-User` and `Google-Agent` may ignore these rules anyway (§1).

### Template C — "Search engines only" (block all AI, keep Google/Bing classic search)

```txt
User-agent: Googlebot
User-agent: bingbot
User-agent: Applebot
User-agent: DuckDuckBot
Allow: /

User-agent: Google-Extended
User-agent: Applebot-Extended
Disallow: /

User-agent: *
Disallow: /
```

Caveat: Googlebot still grounds AI Overviews/AI Mode. The only way out of those while staying indexed is `nosnippet`/`max-snippet`, and that also degrades classic snippets.

### Template D — IETF aipref form (future-proofing; draft only)

```txt
User-Agent: *
Allow: /
Content-Usage: train-ai=n
```

HTTP header form: `Content-Usage: train-ai=n`. Source: draft-ietf-aipref-attach-05 (2026-08-19), with vocabulary from draft-ietf-aipref-vocab-08 (2026-09-14). The vocab defines **AI Training**, **AI Use** ("input to a generative AI model, where the asset is not directly provided by the user") and **Search**, which "does not include the use of assets to generate summaries" and overrides the other categories. The vocab section is marked "does not yet have consensus". No crawler is documented as honouring it yet (UNVERIFIED). Cloudflare's `Content-Signal` is the deployed precursor. Its managed file currently emits `Content-signal: search=yes, ai-train=no, use=reference`, and the meaning of `use=reference` is undocumented on that page (UNVERIFIED).

Content Signals definitions [Cloudflare blog 2025-09-24; managed-robots doc updated 2026-08-03]:
- `search`: "building a search index and providing search results (e.g., returning hyperlinks and short excerpts…). **Search does not include providing AI-generated search summaries.**"
- `ai-input`: "inputting content into one or more AI models (e.g., retrieval augmented generation, grounding, or other real-time taking of content for generative AI search answers)."
- `ai-train`: "training or fine-tuning AI models."
- If a signal is absent, the site "neither grants nor restricts permission". The policy text frames restrictions as EU DSM Directive Art. 4 rights reservations.
- **GEO implication:** for AI-answer visibility, set `ai-input=yes` explicitly. Cloudflare's managed default omits it.

---

## 4. CDN / WAF / platform layer

### 4.1 Cloudflare (the biggest source of accidental AI blocking)

Timeline:
- **2025-07-01 "Content Independence Day"**: new domains default to blocking AI crawlers. Cloudflare also launched managed robots.txt, "block AI bots only on hostnames with ads", and Pay-per-crawl (private beta) [blog.cloudflare.com/content-independence-day-no-ai-crawl-without-compensation; /control-content-use-for-ai-training; /introducing-pay-per-crawl — all 2025-07-01]. The 2025 "Block AI bots" toggle targeted *training* crawlers.
- **2025-05-15 Web Bot Auth** proposal (signed agents) [blog.cloudflare.com/web-bot-auth].
- **2025-08-04**: Perplexity delisted as a verified bot for stealth crawling (undeclared Chrome UA, rotating ASNs, 3–6 M req/day). ChatGPT-User "fetched the robots file and stopped crawling when it was disallowed" [blog.cloudflare.com/perplexity-is-using-stealth-undeclared-crawlers…].
- **2025-09-24 Content Signals Policy**: added to managed robots.txt for 3.8 M domains with `search=yes, ai-train=no` [blog.cloudflare.com/content-signals-policy].
- **2026-02-12 Markdown for Agents** (Pro/Business/Enterprise) [developers.cloudflare.com/changelog/2026-02-12-markdown-for-agents].
- **2026-07-01 new AI traffic taxonomy: Search / Agent / Training.** Options: block all AI bots; block Training+Agent only on ad-monetized pages; allow all. **From 2026-09-15, new domains default to Training + Agent blocked on pages that display ads, with Search allowed.** Crucially, "multi-purpose crawlers such as Googlebot, Applebot, and BingBot will be blocked by customers who have selected to block Training" [blog.cloudflare.com/content-independence-day-ai-options, 2026-07-01]. **This is a classic-SEO landmine**: a site owner ticking "block training" can de-index themselves from Google.
- **July 2026**: Verified bots and signed agents unified in BotBase with a "Direct vs Intermediary access" field. Categories include AI Crawler, AI Search (merged into Search) and AI Assistant (e.g. Perplexity-User, DuckAssistBot) [developers.cloudflare.com/bots/concepts/bot/verified-bots, fetched 2026-09-26].

Features to check in a Cloudflare zone:
| Feature | Where | GEO-relevant setting |
|---|---|---|
| AI Crawl Control (formerly AI Audit) | Dashboard → AI Crawl Control. "Available on all plans", updated 2026-08-14 | Per-crawler Allow/Block. Robots.txt compliance tab shows which crawlers violate. Pay per crawl still "private beta" |
| Block AI bots / Search-Agent-Training categories | Security → Settings → Bot traffic | Make sure **Search** and **Agent** are allowed if you want citations. Don't block "Training" if that silently blocks Googlebot/Bingbot/Applebot (per 2026-07-01 post) |
| Managed robots.txt | Security → Settings → "Set your preference to block training in robots.txt" | Prepends a block disallowing Amazonbot, Applebot-Extended, Bytespider, CCBot, ClaudeBot, Google-Extended, GPTBot and meta-externalagent. Search bots stay allowed. Free-plan zones with no robots.txt get the Content Signals Policy comment text served |
| Bot Fight Mode / Super Bot Fight Mode | Security → Bots | Can JS-challenge non-verified fetchers (Claude-User, MistralAI-User, headless agents). Check the "verified bots" allow |
| Pay per crawl | AI Crawl Control | Returns **HTTP 402** with `crawler-price` header. Crawler opts in with `crawler-exact-price` / `crawler-max-price`. Success returns 200 with `crawler-charged`. Requires Web Bot Auth (Ed25519, JWK) [blog 2025-07-01] |
| Crawler Hints | Caching → Configuration | Sends IndexNow pings on cache MISS/changes |
| Markdown for Agents | AI Crawl Control toggle, or `PATCH /zones/{zone}/settings/content_converter {"value":"on"}` | `Accept: text/markdown` gets `text/markdown; charset=utf-8` plus `x-markdown-tokens`, `x-original-tokens`, `Vary: Accept`. Origin HTML must be ≤2 MB. If the origin sets no `content-signal` header, CF adds `ai-train=yes, search=yes, ai-input=yes`, so **set your own `Content-Signal` response header if you refuse training** [developers.cloudflare.com/fundamentals/reference/markdown-for-agents, fetched 2026-09-26] |

### 4.2 Vercel
- **AI Bots Managed Ruleset**: inactive by default (dashboard label "Allow"). Options are Log or **Deny** (Deny blocks "all traffic identified as coming from AI bots", GPTBot and Claude included).
- **Bot Protection Managed Ruleset**: inactive by default ("Off"). In **Challenge** mode it "will serve a JavaScript challenge to traffic that is unlikely to be a browser". Verified bots are excluded.
- Custom rules run before managed rulesets. Use a **Bypass** custom rule on UA to exempt a fetcher.
Source: vercel.com/docs/vercel-firewall/vercel-waf/managed-rulesets (last_updated 2026-09-10). Risk: an unverified user-triggered fetcher (for example a new agent) will fail a JS challenge.

### 4.3 Netlify
- "User Agent Blocker" extension (Edge Function). **Not on by default**. You choose AI and SEO crawler presets, and "this list does not include all possible AI crawlers" [docs.netlify.com/build/build-with-ai/block-ai-crawlers, updated 2026-09-18]. Audit `netlify.toml`, edge functions and installed extensions.

### 4.4 Akamai / Fastly / others
- Akamai Bot Manager sorts AI traffic into training crawlers, search crawlers and fetchers, and lets you act per bot (akamai.com blog "Managing AI Bots as Part of Your Overall Bot Management Strategy", undated in fetch; secondary summary). Akamai reports AI bot traffic up over 300% from 2025 to early 2026 and advises caution with blanket blocks (secondary, UNVERIFIED).
- Fastly: bot management product exists. Default AI treatment is UNVERIFIED.
- WordPress security plugins (Wordfence, etc.), Shopify's platform robots.txt, Wix/Squarespace "block AI crawlers" toggles, and hosting-level ModSecurity rules are frequent hidden blockers (UNVERIFIED individually; worth checking).

### 4.5 Web Bot Auth (signed agents)
- Built on RFC 9421 HTTP Message Signatures. Headers are `Signature-Input`, `Signature` and `Signature-Agent`. Keys are published at `/.well-known/http-message-signatures-directory`, and the tag is `"web-bot-auth"` [Cloudflare blog 2025-05-15].
- Example: `Signature-Input: sig=("@authority" "signature-agent");created=1700000000;expires=1700011111;keyid="ba3e64==";tag="web-bot-auth"`.
- Signers: ChatGPT agent (`Signature-Agent: "https://chatgpt.com"`, with quotes) [simonwillison.net 2025-08-04]; Google-Agent is "experimenting with the Web Bot Auth protocol" [Google user-triggered fetchers, 2026-08-19].
- IETF: draft-ietf-webbotauth-httpsig-protocol; per search summaries it was adopted as Standards Track on 2026-09-01 (UNVERIFIED primary). Companion "Signature Agent Card" draft (draft-meunier-webbotauth-registry).
- Site-side action: **don't strip or reject unknown `Signature*` headers**. If you run your own bot rules, allowlist verified signatures instead of UA strings.

---

## 5. JavaScript rendering

### 5.1 Evidence
| Fetcher | Executes JS? | Source |
|---|---|---|
| Googlebot (so AI Overviews / AI Mode / Gemini grounding) | Yes. Evergreen Chromium, deferred render queue | Google JS SEO basics (fetched 2026-09-26); Vercel 2024-12-17 |
| Applebot | Yes ("renders webpage content in a browser"). Blocking CSS/JS in robots.txt can break it | support.apple.com/119829 |
| GPTBot, OAI-SearchBot, ChatGPT-User | No. Fetches JS files (11.5% of GPTBot requests) but doesn't run them | Vercel/MERJ 2024-12-17 |
| ClaudeBot | No (23.84% of requests are JS files, not executed) | Vercel 2024-12-17 |
| PerplexityBot, Meta-ExternalAgent, Bytespider | No | Vercel 2024-12-17, restated by 2026 secondary sources |
| Bingbot | Renders (knowledge). Copilot extraction depth UNVERIFIED | — |
| Browser agents (ChatGPT agent/Atlas, Comet, Claude for Chrome, Google-Agent) | Yes, full browser. But they read the DOM/accessibility tree and depend on stable semantics | OpenAI Atlas guidance, Oct 2025 (via Roselli critique) |

Vercel's is still the most-cited measurement. 2026 secondary reviews say no newer primary study contradicts it (getpassionfruit/searchoptimo 2026; secondary). OAI-SearchBot's UA contains `Chrome/131`, but OpenAI doesn't claim it renders (UNVERIFIED either way). **Assume no JS for every non-Google, non-Apple AI crawler.**

AI crawlers also ran only from US locations in 2024 (ChatGPT from Des Moines and Phoenix, Claude from Columbus) [Vercel]. **Geo-blocking or geo-redirecting US traffic hides a site from them.**

### 5.2 What breaks for AI fetchers
- CSR SPAs (CRA, plain Vite React/Vue/Svelte SPA) ship an empty `<div id="root">`, so the AI crawler sees no content.
- Content that's only in client components after hydration (`useEffect` fetches, `"use client"` data loading, SWR/React Query on first paint).
- Tabs and accordions whose panels are fetched on click (content missing from HTML). Tabs rendered in HTML but hidden with CSS are fine.
- Infinite scroll without paginated `<a href>` URLs.
- "Load more" buttons and JS-only links (`onClick` navigation, `<div>` links). Google: "Googlebot can only discover your links if they are `<a>` HTML elements with an `href` attribute."
- Lazy-loaded text via IntersectionObserver. Lazy images should keep `src`/`srcset` with `loading="lazy"`.
- Titles, meta descriptions, canonicals and JSON-LD injected client-side. Put them in server HTML.
- Soft-404s in SPAs (200 status for missing pages). Google advises a server 404 or `noindex`. JS that *removes* `noindex` may never run, because Google may skip rendering noindexed pages.
- Consent managers that replace the body until consent is given.

### 5.3 Per-framework guidance
| Stack | Default | Do this |
|---|---|---|
| Next.js App Router | RSC/SSR by default | Keep content in Server Components. Fetch data server-side (`async` components). Avoid `"use client"` wrappers around article bodies. Use `generateMetadata` and emit JSON-LD in server output. `export const dynamic='force-static'` or ISR for content pages. Don't gate content behind `Suspense` fallbacks that stream only after long waits (check with `curl`) |
| Next.js Pages Router | depends | Use `getStaticProps`/`getServerSideProps`. Never `useEffect` fetch for primary content |
| Nuxt 3/4 | SSR (`ssr: true`) | Use `useAsyncData`/`useFetch` (SSR-aware) and `routeRules` prerender/ISR. Avoid `<ClientOnly>` around content |
| SvelteKit | SSR | Use `load` in `+page.server.ts`, `export const prerender = true` for static pages. Don't set `ssr = false` on content routes |
| Remix / React Router 7 | SSR | Use `loader` data. Don't use clientLoader-only content |
| Astro | Static HTML | Ideal. Keep islands for interactivity only (`client:*`), content in `.astro`/MD |
| Angular | CSR unless SSR added | Add `@angular/ssr` (hydration) or prerender |
| Vue/React SPA (Vite, CRA) | CSR, empty HTML | Migrate to a meta-framework, or prerender at build (vite-plugin-ssr/vike, `react-snap`-style prerender, Astro). Last resort: dynamic rendering or a prerender proxy for bot UAs. Google calls dynamic rendering a workaround, not a long-term solution (knowledge; Google JS SEO docs) |
| Gatsby / Hugo / Eleventy / Jekyll | Static | Fine. Check that client-only plugins don't hold content |
| WordPress / headless CMS | Server HTML | Fine unless page builders lazy-render via JS. Check `curl` output |
| Webflow / Framer / Wix | Mostly server HTML | Check CMS collection lists, tabs and "load more" in `curl` output |

**Acceptance test:** `curl -sA "GPTBot" URL | sed 's/<[^>]*>//g'` should contain the H1, the first answer paragraph, prices/specs, FAQ answers, author and date. Also compare the word count against the rendered DOM (Playwright). A gap of more than about 10% means content is hidden from AI.

---

## 6. Detection checklist: "is my site accidentally blocking AI?"

### 6.1 Quick probes (run from a non-residential IP; also from a US region)
```bash
URL=https://www.example.com/some-article
for UA in \
 "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; GPTBot/1.4; +https://openai.com/gptbot" \
 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36; compatible; OAI-SearchBot/1.4; +https://openai.com/searchbot" \
 "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; ChatGPT-User/1.0; +https://openai.com/bot" \
 "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; ClaudeBot/1.0; +claudebot@anthropic.com)" \
 "Claude-User/1.0" "Claude-SearchBot/1.0" \
 "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)" \
 "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)" \
 "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)" \
 "DuckAssistBot/1.2; (+http://duckduckgo.com/duckassistbot.html)" \
 "meta-externalagent/1.1" "Amzn-SearchBot/0.1" "MistralAI-User/1.0" ; do
  printf '%-40.40s ' "$UA"
  curl -s -o /tmp/body.html -w '%{http_code} %{size_download}B %{time_starttransfer}s ' -A "$UA" -L "$URL"
  grep -qiE 'cf-chl|challenge-platform|captcha|Just a moment|Access denied|px-captcha|_Incapsula_' /tmp/body.html && echo CHALLENGE || echo ok
done
curl -s -o /dev/null -w 'robots %{http_code} %{content_type}\n' https://www.example.com/robots.txt
curl -sI -H 'Accept: text/markdown' "$URL" | grep -iE 'content-type|x-markdown-tokens|vary|content-signal'
```
Caveats: spoofed-UA tests hit **UA rules only**. Cloudflare/Akamai verify real bots by IP, so a spoofed "Googlebot" from your laptop may be *blocked* while the real one passes (and vice versa for "verified bots" allowlists). Confirm with:
- **Cloudflare**: AI Crawl Control → crawler list (requests, allowed vs blocked, robots.txt violations); Security Events filtered by `cf.verified_bot_category`.
- **Vercel**: Firewall → Overview/Observability per rule.
- **Google Search Console**: URL Inspection (live test) plus Crawl stats → by response.
- **Bing Webmaster Tools**: URL Inspection / Site Scan. Bing also has an AI Performance/Copilot citations report (UNVERIFIED name).
- **Server logs**: grep for 403/429/503 by AI UA (§8).

### 6.2 Checklist
- [ ] `/robots.txt` returns 200 `text/plain` to every UA (not 403, not a challenge, not an HTML 404 page), is under 500 KiB, and has no stray `Disallow: /` in a `*` group left over from staging.
- [ ] Named UA groups repeat the shared disallows. No accidental blocking of `Googlebot`/`bingbot`/`Applebot` in "AI block" lists.
- [ ] Cloudflare: AI Crawl Control shows Search/Agent crawlers **Allowed**. Ad-page default (from 2026-09-15) reviewed. The "block Training" choice doesn't collaterally block Googlebot/Bingbot/Applebot. Managed robots.txt contents are intentional. Bot Fight Mode isn't challenging verified bots.
- [ ] Vercel AI Bots ruleset isn't `Deny` (unless intended). Bot Protection Challenge isn't hitting fetchers. Netlify UA Blocker presets reviewed.
- [ ] No geo-block or geo-redirect for US data-centre IPs (Des Moines, Phoenix, Columbus). No forced locale redirect by `Accept-Language` without an `x-default`.
- [ ] No cookie wall or consent overlay that removes body content from the HTML. Paywalled content uses `isAccessibleForFree` + `hasPart.cssSelector` markup (Google paywall doc, updated 2026-09-08) so gating isn't treated as cloaking.
- [ ] Rate limits (429) aren't set so low that crawl bursts fail. Prefer `Crawl-delay` for Anthropic, or CDN caching.
- [ ] Meta robots / `X-Robots-Tag`: no unintended `noindex`, `nosnippet`, `max-snippet:0`, `noarchive`, `nocache`.
- [ ] Raw HTML contains the main content (§5 acceptance test).
- [ ] TTFB is low for bots. Serve cached HTML at the edge. AI fetchers' timeouts aren't published (UNVERIFIED). User-triggered fetchers run while a user waits, so slow origins (over 2–5 s) plausibly get dropped (UNVERIFIED, reasoned).
- [ ] 404s are real 404s, redirects are single-hop 301s, and sitemaps list only 200 canonical URLs (AI crawlers spent 34.8% of fetches on 404s and 14.4% on redirects [Vercel]).

---

## 7. llms.txt, llms-full.txt and markdown delivery

### 7.1 llms.txt spec (llmstxt.org, Jeremy Howard, proposed 2024-09-03, page modified 2026-08-10)
Format, in order: optional BOM; **H1 with the site/project name (the only required element)**; blockquote summary; optional free markdown sections; zero or more **H2 "file lists"** of `- [name](url): note` links. An `## Optional` section marks links that can be skipped when context is short. Companion convention: provide a clean markdown copy of each page at the same URL with `.md` appended (`page.html.md`), or with the extension replaced (`index.html.md` for directory URLs). `llms-full.txt` (a single file with the full concatenated docs) is a widespread community convention (Mintlify/docs platforms), not part of the llmstxt.org text (the fetch found no mention).

```markdown
# Example Co

> Example Co makes X for Y. This file lists the canonical, citable pages.

## Docs
- [Pricing](https://www.example.com/pricing.md): plans, limits, currency
- [API reference](https://www.example.com/docs/api.md): endpoints and auth

## Optional
- [Changelog](https://www.example.com/changelog.md)
```

### 7.2 Evidence of use
- **Google**: "You don't need to create new machine readable files, AI text files, markup, or Markdown to appear in Google Search (including its generative AI capabilities)… keeping one will neither harm nor help… as Google Search ignores them" (developers.google.com/search/docs/fundamentals/ai-optimization-guide; guide announced May 2026 on the Search Central blog, llms.txt clarification reported as added 2026-06-15, secondary). Google's guide also says there's no need to "chunk" content and no special schema is required.
- **Ahrefs (published 2026-06-15)**: 137,210 domains. 28% publish llms.txt, and **97% of those got zero requests in May 2026**. Of the requests that did happen, 19.5% were AI bots (agentic infra 10.5%, training crawlers like GPTBot 5.3%, assistants 2.5%, retrieval bots like PerplexityBot 1.1%) and 77% were non-AI tools. "Zero AI bots 'go looking' for llms.txt files that don't exist."
- Individual log studies (saaslinks.net, ezy.ai, 2026; secondary) found AI crawlers fetch robots.txt constantly and llms.txt almost never.
- No major answer engine (OpenAI, Anthropic, Perplexity, Google, Microsoft) documents consuming llms.txt for search/citation (UNVERIFIED negative; none found). Coding agents (Claude Code, Cursor, etc.) do fetch docs llms.txt when pointed at it.
- Recommendation: publish llms.txt only as a low-cost curated index (docs/dev-tool sites benefit most). Don't block anything on it, and don't treat it as a GEO lever.

### 7.3 Markdown content negotiation (more useful than llms.txt)
- Log evidence: 1,421 markdown requests over 44 days (2026-03-07 to 04-19). "Claude" was 35% (500 requests), then headless Chrome pools (639) and axios pipelines (211) [suganthan.com/blog/cloudflare-markdown-for-agents].
- Cloudflare Markdown for Agents: §4.1. Test with `curl URL -H "Accept: text/markdown"`.
- Vercel pattern (blog 2026-02-03, "Making agent-friendly pages with content negotiation"): rewrite on `Accept` to a markdown route handler. Blog payload fell 99.37% (500 KB to 3 KB). They also publish a markdown sitemap (`/blog/sitemap.md`).

```ts
// next.config.ts — serve markdown when the client asks for it
export default {
  async rewrites() {
    return {
      beforeFiles: [
        {
          source: '/blog/:path*',
          has: [{ type: 'header', key: 'accept', value: '(.*)text/markdown(.*)' }],
          destination: '/blog/md/:path*',
        },
      ],
    };
  },
};
// app/blog/md/[[...slug]]/route.ts
export async function GET(_req: Request, { params }: { params: Promise<{ slug?: string[] }> }) {
  const { slug = [] } = await params;
  const md = await renderPostAsMarkdown(slug.join('/')); // CMS rich text -> markdown
  return new Response(md, {
    headers: {
      'Content-Type': 'text/markdown; charset=utf-8',
      'Vary': 'Accept',
      'Link': `<https://www.example.com/blog/${slug.join('/')}>; rel="canonical"`,
      // 'Content-Signal': 'search=yes, ai-input=yes, ai-train=no',
    },
  });
}
```
Rules: always send `Vary: Accept` so caches don't serve markdown to browsers. Add a `rel="canonical"` Link header pointing at the HTML URL so `.md` variants don't compete in classic search. Optionally advertise `<link rel="alternate" type="text/markdown" href="/page.md">` in the HTML head. Keep the markdown content identical in substance to the HTML (to avoid cloaking concerns).

---

## 8. Agentic web standards (making sites operable, not just readable)

| Standard | Owner / date | What a site does | Status |
|---|---|---|---|
| **MCP** (Model Context Protocol) server | Anthropic, open spec (Nov 2024), now multi-vendor | Expose search, product lookup, booking etc. as tools at e.g. `https://example.com/mcp` (streamable HTTP) | Widely supported by assistants. Discovery conventions for websites are still informal (UNVERIFIED) |
| **WebMCP** | W3C Web ML CG, Google + Microsoft; CG draft 2026-04-23 | In-page tools for browser agents. **Declarative**: annotate existing `<form>` with `toolname` / `tooldescription` attributes. **Imperative**: register JS tools (API moving from `navigator.modelContext` to `document`, per secondary) | Chrome **origin trial from Chrome 149**; flag `chrome://flags/#enable-webmcp-testing`. Requires Permissions Policy `tools` (default `self`) and origin isolation [developer.chrome.com/docs/ai/webmcp, fetched 2026-09-26]. Firefox/Safari have no committed timeline (secondary) |
| **NLWeb** | Microsoft (R.V. Guha), Build 2025 | `/ask` (natural-language query to schema.org JSON) and `/mcp`, built on your schema.org + RSS | Reference impl github.com/nlweb-ai/NLWeb. Cloudflare AI Search reportedly added NLWeb support early 2026 (secondary, UNVERIFIED) |
| **Agentic Commerce Protocol (ACP)** | OpenAI + Stripe, launched with ChatGPT Instant Checkout (Etsy first, Shopify next; announced 2025-09-29 per Stripe newsroom, knowledge-dated) | Product feed (CSV/TSV/XML/JSON: IDs, price, inventory, media, fulfillment) + Agentic Checkout API + Delegated Payment spec (Stripe Shared Payment Token) | developers.openai.com/commerce. Approved partners. Out of PCI scope |
| **Universal Commerce Protocol (UCP)** | Google + Shopify, Etsy, Wayfair, Target, Walmart; announced NRF 2026-01-11 | Publish a business profile manifest at **`/.well-known/ucp`** (version, services, capabilities such as checkout, fulfillment, discounts). Implement at least Checkout | developers.googleblog.com "Under the hood: UCP"; shopify.engineering/ucp (secondary summaries) |
| **AP2 (Agent Payments Protocol)** | Google, 2025-09-16, 60+ partners | Signed Intent/Cart/Payment "mandates" (W3C Verifiable Credentials). An extension of A2A/MCP. A2A x402 extension for crypto | cloud.google.com blog "Announcing Agent Payments Protocol (AP2)" |
| **A2A (Agent2Agent)** | Google, now Linux Foundation | Agent card at `/.well-known/agent.json` (path per knowledge; UNVERIFIED current version) for agent-to-agent tasks | Mostly B2B/agent platforms |
| **Web Bot Auth** | IETF webbotauth WG | Verify signed agents (§4.5) | Standards-track draft |
| **Pay per crawl / HTTP 402, x402** | Cloudflare; Coinbase x402 | Monetise crawler access | Private beta / emerging |

### 8.1 Making pages operable by browser agents (ChatGPT agent/Atlas, Perplexity Comet, Claude for Chrome, Gemini agent/Google-Agent)
OpenAI told site owners (Atlas launch, 2025-10-21) that "website owners can add ARIA tags to improve how ChatGPT agent works for their websites in Atlas" (quoted in adrianroselli.com, 2025-10). Accessibility experts caution that **native semantic HTML beats ARIA** (the first rule of ARIA) and that ARIA misuse lowers accessibility [Roselli, 2025-10]. Practical rules:
- Use native elements: `<button>`, `<a href>`, `<form>`, `<label for>`, `<select>`, `<input type=...>` with `name`, `autocomplete` and `inputmode`. Avoid clickable `<div>`s.
- Give every control a stable accessible name (visible label, or `aria-label` only when there's no visible text). Keep names stable across deploys. Don't use hashed or random `id`s as the only hook.
- Landmarks: `<header> <nav> <main> <aside> <footer>`, one `<h1>`, logical heading order.
- State via native attributes (`disabled`, `aria-expanded`, `aria-current`, `aria-invalid` + `aria-describedby` for errors).
- Deterministic flows: no hover-only menus, no drag-only controls, no canvas-only UIs. Put prices, stock and options as text in the DOM. Use URL-addressable states (filters in query strings).
- Avoid CAPTCHAs on read paths. Don't make checkout depend on third-party iframes without labels.
- Don't block signed agents. Consider allowing `Signature-Agent`-verified traffic past bot challenges.
- For commerce: keep `Product`/`Offer` JSON-LD consistent with visible price and availability (feeds for ACP/UCP must match the page).

---

## 9. Discovery and freshness plumbing

- **XML sitemaps**: max 50,000 URLs / 50 MB uncompressed per file. Use a sitemap index. Google "uses the `<lastmod>` value if it's consistently and verifiably… accurate", meaning the last *significant* change (main content, structured data), not the copyright year. Google ignores `<priority>` and `<changefreq>` [developers.google.com/.../build-sitemap, fetched 2026-09-26]. Emit lastmod from the content's real `updated_at`, never from build time. List only canonical 200 URLs. Reference the sitemap in robots.txt.
- **IndexNow**: participants are **Amazon, Bing, Naver, Seznam.cz, Yandex, Yep**, and submissions are shared across all of them. Google does not participate. Key file `/{key}.txt` (8–128 chars, `[A-Za-z0-9-]`) [indexnow.org/faq, fetched 2026-09-26]. Bing feeds Copilot, and reportedly ChatGPT search partly relies on Bing (UNVERIFIED), so IndexNow is the fastest freshness lever for non-Google AI surfaces. Cloudflare **Crawler Hints** automates IndexNow pings from cache signals.
```bash
curl -X POST https://api.indexnow.org/indexnow -H 'Content-Type: application/json' -d '{
 "host":"www.example.com","key":"<KEY>","keyLocation":"https://www.example.com/<KEY>.txt",
 "urlList":["https://www.example.com/new-page","https://www.example.com/updated-page"]}'
```
- **RSS/Atom**: Google's `FeedFetcher-Google` crawls feeds for Google News/WebSub. NLWeb ingests RSS. Expose `<link rel="alternate" type="application/rss+xml">` with full-text items and real `updated` dates.
- **HTTP status and caching**: real 404/410 for gone pages. Single-hop 301 for moves (no JS redirects, no meta refresh). Use `ETag`/`Last-Modified` and honour `If-Modified-Since` with 304 (cuts bot load). Put `Cache-Control` on HTML so the CDN can serve bots fast. 503 + `Retry-After` for maintenance (never 200 maintenance pages).
- **Canonicalization**: one canonical URL per content item in server HTML (`<link rel="canonical">`). Consistent trailing slash, lowercase, https, host. Strip tracking params (AI answers append `utm_source=chatgpt.com` and similar: knowledge, widely observed, UNVERIFIED in docs this session). Canonical must not point at a JS-only or blocked URL. Markdown twins get a `Link: rel=canonical` header.
- **Speed/TTFB**: no vendor publishes AI fetcher timeouts (UNVERIFIED). Edge-cached SSR/SSG HTML with TTFB under ~500 ms and HTML under ~2 MB (Cloudflare markdown conversion limit is 2 MB; Google truncates indexing of very large HTML, knowledge) is a safe target.
- **Paywalls/logins**: content behind login is invisible to all AI crawlers. For metered/paywalled content, show the lead/answer summary publicly and mark the gated part with `isAccessibleForFree:false` + `hasPart.cssSelector` (Google, 2026-09-08). Serving full content to Googlebot only, without markup, is cloaking.
- **Cookie walls / consent**: render content in HTML underneath the banner. Don't redirect bots to a consent page. Bots don't click "accept".
- **Bot-challenge pages**: a 200 "Just a moment…" page is worse than a 403, because it can be ingested as your content. Monitor for challenge HTML in bot responses (§6.1 grep).

---

## 10. Server-log analysis for AI bots

### 10.1 Classify
```bash
# Combined log format; count hits and status codes per AI UA
grep -Eio 'GPTBot|OAI-SearchBot|ChatGPT-User|OAI-AdsBot|ClaudeBot|Claude-SearchBot|Claude-User|PerplexityBot|Perplexity-User|Google-Agent|Google-GeminiNotebook|GoogleOther|Google-CloudVertexBot|Googlebot|bingbot|Applebot|meta-externalagent|meta-externalfetcher|meta-webindexer|Amazonbot|Amzn-SearchBot|Amzn-User|DuckAssistBot|CCBot|MistralAI-[A-Za-z]+|Bytespider|cohere[-a-z]*|DeepSeekBot|GrokBot' access.log \
 | sort | uniq -c | sort -rn

awk -F'"' '/GPTBot|ClaudeBot|OAI-SearchBot|PerplexityBot|ChatGPT-User|Claude-User/ {split($3,a," "); print a[1], $6}' access.log \
 | awk '{s[$1" "$2]++} END{for(k in s) print s[k], k}' | sort -rn | head    # status x UA

# Requests carrying signed-agent headers (needs header logging)
grep -i 'signature-agent' access.log | head
```

### 10.2 Verify (IP ranges + reverse DNS)
```python
# verify_bots.py — tag each log IP with the vendor list it belongs to (lists fetched live 2026-09-26)
import ipaddress, json, urllib.request, sys, re, socket
LISTS = {
 "GPTBot": "https://openai.com/gptbot.json",
 "OAI-SearchBot": "https://openai.com/searchbot.json",
 "ChatGPT-User": "https://openai.com/chatgpt-user.json",
 "OAI-AdsBot": "https://openai.com/adsbot.json",
 "Anthropic": "https://claude.com/crawling/bots.json",
 "PerplexityBot": "https://www.perplexity.com/perplexitybot.json",
 "Perplexity-User": "https://www.perplexity.com/perplexity-user.json",
 "Google-common": "https://developers.google.com/static/crawling/ipranges/common-crawlers.json",
 "Google-agents": "https://developers.google.com/static/crawling/ipranges/user-triggered-agents.json",
 "Applebot": "https://search.developer.apple.com/applebot.json",
 "bingbot": "https://www.bing.com/toolbox/bingbot.json",
 "DuckAssistBot": "https://duckduckgo.com/duckassistbot.json",
 "CCBot": "https://index.commoncrawl.org/ccbot.json",
 "MistralAI-User": "https://mistral.ai/mistralai-user-ips.json",
}
def nets(url):
    data = json.load(urllib.request.urlopen(url, timeout=20))
    out = []
    for p in data.get("prefixes", []):
        for k in ("ipv4Prefix", "ipv6Prefix"):
            if k in p: out.append(ipaddress.ip_network(p[k], strict=False))
    return out
TABLE = {name: nets(u) for name, u in LISTS.items()}
def owner(ip):
    a = ipaddress.ip_address(ip)
    return [n for n, ns in TABLE.items() if any(a in net for net in ns)]
def rdns_ok(ip, suffixes):          # forward-confirmed reverse DNS
    try:
        host = socket.gethostbyaddr(ip)[0]
        return host.endswith(suffixes) and ip in socket.gethostbyname_ex(host)[2]
    except Exception: return False
for line in sys.stdin:               # usage: cat access.log | python verify_bots.py
    ip = line.split()[0]; ua = re.search(r'"([^"]*)"\s*$', line)
    ua = ua.group(1) if ua else ""
    claims = re.findall(r'GPTBot|OAI-SearchBot|ChatGPT-User|ClaudeBot|Claude-\w+|PerplexityBot|Perplexity-User|Googlebot|Google-Agent|bingbot|Applebot|CCBot|DuckAssistBot|MistralAI-\w+', ua)
    if claims:
        o = owner(ip)
        if not o and "Googlebot" in claims: o = ["Google(rDNS)"] if rdns_ok(ip, (".googlebot.com", ".google.com", ".googleusercontent.com")) else []
        if not o and "Applebot" in claims:  o = ["Apple(rDNS)"]  if rdns_ok(ip, (".applebot.apple.com",)) else []
        print(("VERIFIED " if o else "SPOOFED? ") + ip, claims, o)
```
Reverse-DNS patterns: Google `crawl-*.googlebot.com`, `rate-limited-proxy-*.google.com`, `*.gae.googleusercontent.com`, `google-proxy-*.google.com` (Google verifying-googlebot doc). Apple `*.applebot.apple.com`. Common Crawl `*.crawl.commoncrawl.org`. Bing `*.search.msn.com` (knowledge). Signed agents: verify `Signature` against the key directory named in `Signature-Agent`.

### 10.3 Metrics worth tracking per AI bot
Hits/day; unique URLs; status mix (200/3xx/4xx/5xx/403/429); share of hits on sitemap URLs vs orphan URLs; median response time and bytes; robots.txt fetch frequency; first-seen lag after publish (freshness); for user-triggered agents, which pages get fetched (a proxy for which pages get cited). Join with referrals from `chatgpt.com`, `perplexity.ai`, `copilot.microsoft.com`, `gemini.google.com`, `claude.ai` in analytics.

### 10.4 Tools
Cloudflare AI Crawl Control (per-crawler analytics and robots.txt violations) and Cloudflare Radar AI Insights; Vercel Firewall observability; Google Search Console crawl stats; Bing Webmaster Tools; log analysers (Screaming Frog Log File Analyser, GoAccess, Botify/Oncrawl/Lumar log modules, Conductor, Profound Agent Analytics, Dark Visitors / knownagents.com agent directory, Ahrefs bot analytics). Commercial-tool capability claims are UNVERIFIED this session. Maintain block/allow lists from github.com/ai-robots-txt/ai.robots.txt (it ships robots.txt, nginx, Apache, Caddy and HAProxy snippets). Use it as a **UA reference**, not as a default block list, for a GEO site.

---

## 11. Open questions / marked UNVERIFIED
- Bing's official wording on `noarchive`/`nocache` for Copilot (bing.com help is JS-rendered; only secondary sources read).
- Whether OAI-SearchBot now renders JS (its UA advertises Chrome/131; no statement found).
- Timeouts of AI fetchers. No vendor publishes them.
- Meaning of Cloudflare's `use=reference` content signal.
- IETF Web Bot Auth Standards Track adoption date (2026-09-01) comes from a search summary only.
- ByteDance/xAI/DeepSeek/Cohere crawler documentation. None official found.
- The Cloudflare 2026-07-01 statement that blocking "Training" blocks Googlebot/Applebot/Bingbot is quoted from the blog as fetched, but confirm in the dashboard before advising, because the operational details (e.g. whether Googlebot is blocked only on ad pages under the default) were not specified.
- ACP launch date (2025-09-29) is from knowledge plus Stripe newsroom titles. The openai.com page returned 403.

---

## Sources (fetched 2026-09-26 unless noted)
- OpenAI crawlers: https://developers.openai.com/api/docs/bots ; change log coverage https://ppc.land/openai-revises-chatgpt-crawler-documentation-with-significant-policy-changes/ (Dec 2025)
- Anthropic: https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler ; IPs https://claude.com/crawling/bots.json (creationTime 2026-08-18)
- Google common crawlers: https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers
- Google user-triggered fetchers (updated 2026-08-19): https://developers.google.com/search/docs/crawling-indexing/google-user-triggered-fetchers
- Google verification: https://developers.google.com/search/docs/crawling-indexing/verifying-googlebot
- Google robots.txt spec: https://developers.google.com/search/docs/crawling-indexing/robots/robots_txt
- Google AI features (updated 2025-12-10): https://developers.google.com/search/docs/appearance/ai-features
- Google AI optimization guide (2026): https://developers.google.com/search/docs/fundamentals/ai-optimization-guide ; blog https://developers.google.com/search/blog/2026/05/a-new-resource-for-optimizing
- Google JS SEO basics: https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics
- Google sitemaps: https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- Google paywalled content (updated 2026-09-08): https://developers.google.com/search/docs/appearance/structured-data/paywalled-content
- Apple: https://support.apple.com/en-us/119829
- Meta: https://developers.facebook.com/docs/sharing/webmasters/web-crawlers/
- Amazon: https://developer.amazon.com/amazonbot
- Perplexity: https://docs.perplexity.ai/guides/bots
- DuckDuckGo: https://duckduckgo.com/duckduckgo-help-pages/results/duckassistbot
- Common Crawl: https://commoncrawl.org/ccbot
- Mistral: https://docs.mistral.ai/robots
- ai.robots.txt list: https://github.com/ai-robots-txt/ai.robots.txt
- Bing controls (secondary): https://better-robots.com/blog/bing-noarchive-nocache-vs-robots-txt ; https://searchengineland.com/bing-adds-controls-for-webmasters-to-disallow-their-content-in-bing-chat-432174 (2023, 403 on fetch)
- nohacks AI UA landscape (2026-08-08): https://nohacks.co/blog/ai-user-agents-landscape-2026
- Cloudflare 2025-07-01: https://blog.cloudflare.com/content-independence-day-no-ai-crawl-without-compensation/ ; https://blog.cloudflare.com/control-content-use-for-ai-training/ ; https://blog.cloudflare.com/introducing-pay-per-crawl/
- Cloudflare 2026-07-01 taxonomy: https://blog.cloudflare.com/content-independence-day-ai-options/
- Cloudflare Content Signals (2025-09-24): https://blog.cloudflare.com/content-signals-policy/
- Cloudflare managed robots.txt (updated 2026-08-03): https://developers.cloudflare.com/bots/additional-configurations/managed-robots-txt/
- Cloudflare AI Crawl Control (updated 2026-08-14): https://developers.cloudflare.com/ai-crawl-control/
- Cloudflare verified bots: https://developers.cloudflare.com/bots/concepts/bot/verified-bots/
- Cloudflare Markdown for Agents: https://developers.cloudflare.com/fundamentals/reference/markdown-for-agents ; changelog 2026-02-12
- Cloudflare Crawler Hints: https://developers.cloudflare.com/cache/advanced-configuration/crawler-hints/
- Cloudflare Web Bot Auth (2025-05-15): https://blog.cloudflare.com/web-bot-auth/
- Cloudflare on Perplexity (2025-08-04): https://blog.cloudflare.com/perplexity-is-using-stealth-undeclared-crawlers-to-evade-website-no-crawl-directives/
- IETF aipref: https://www.ietf.org/archive/id/draft-ietf-aipref-vocab-08.txt (2026-09-14); https://www.ietf.org/archive/id/draft-ietf-aipref-attach-05.txt (2026-08-19)
- IETF webbotauth: https://datatracker.ietf.org/doc/draft-ietf-webbotauth-httpsig-protocol/
- ChatGPT agent signatures (2025-08-04): https://simonwillison.net/2025/Aug/4/chatgpt-agents-user-agent/
- Vercel AI crawler study (2024-12-17): https://vercel.com/blog/the-rise-of-the-ai-crawler
- Vercel content negotiation (2026-02-03): https://vercel.com/blog/making-agent-friendly-pages-with-content-negotiation
- Vercel WAF managed rulesets (2026-09-10): https://vercel.com/docs/vercel-firewall/vercel-waf/managed-rulesets
- Netlify UA blocker (2026-09-18): https://docs.netlify.com/build/build-with-ai/block-ai-crawlers/
- Akamai AI bots (secondary): https://www.akamai.com/blog/security/managing-ai-bots-part-overall-bot-management-strategy
- llms.txt spec: https://llmstxt.org/
- Ahrefs llms.txt study (2026-06-15): https://ahrefs.com/blog/llmstxt-study/
- Markdown log study (Mar–Apr 2026): https://suganthan.com/blog/cloudflare-markdown-for-agents/
- IndexNow: https://www.indexnow.org/faq
- WebMCP: https://developer.chrome.com/docs/ai/webmcp ; https://github.com/webmachinelearning/webmcp
- NLWeb: https://github.com/nlweb-ai/NLWeb
- ACP: https://developers.openai.com/commerce ; https://stripe.com/newsroom/news/stripe-openai-instant-checkout
- UCP: https://developers.googleblog.com/under-the-hood-universal-commerce-protocol-ucp/ ; https://shopify.engineering/ucp
- AP2: https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol
- Atlas/ARIA critique (2025-10): https://adrianroselli.com/2025/10/openai-aria-and-seo-making-the-web-worse.html
