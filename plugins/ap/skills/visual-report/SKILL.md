---
name: visual-report
description: Build a report with genuine embedded images — real screenshots, rendered PDF pages, live-app captures — organized as a report.html file plus a sibling images/ folder, verified end-to-end so no image is ever faked, placeholder, or silently skipped. Use whenever the user asks for a report, writeup, documentation, or before/after comparison that should show real visual evidence — especially bug-fix reports, audit findings, QA/verification writeups, client-facing proof-of-work, or "show me before and after" requests — even if they don't say "HTML" or "images" explicitly. If real screenshots or renderable evidence exist or are obtainable, reach for this skill instead of writing a plain text summary. Local files only, not a shareable link — if the user wants a hosted/shareable page instead, use the Artifact tool (see artifact-design skill) since that requires a different, base64-embedded approach.
---

# Visual report

A report is only as good as the evidence in it. This skill produces a `report.html` plus a sibling `images/` folder — a self-contained, inspectable directory where every image is something you actually captured, converted, or were handed, and every claim in the text is backed by a real picture sitting right next to it.

## The one rule everything else follows

**Every image must be genuine.** A real screenshot, a real rendered page from a real PDF, a real file the user gave you. Never a placeholder box, never a "here's roughly what it would look like" mockup, never stock or generic imagery standing in for the real thing.

If you can't get a real image for something, say so and stop asking the user — don't quietly fall back to describing it in prose instead. A sentence like "the dashboard showed an error here" where an actual screenshot was expected isn't a lesser version of the report, it's a broken promise the report makes to the reader (that everything shown was verified, not narrated). If a source file goes missing mid-task — you deleted it, overwrote it, whatever — regenerate it for real rather than reaching for the description-as-substitute shortcut.

This matters more than it might seem. A report with genuinely embedded evidence is something a reader can trust without re-checking; a report that quietly substitutes description for a missing image looks identical at a glance but earns exactly the wrong kind of trust.

## Folder structure

```
<report-name>/
  report.html
  images/
    01-<short-description>.png
    02-<short-description>.jpeg
    ...
```

Number the image filenames in the order they appear in the narrative — it keeps the `images/` folder self-explanatory even away from the HTML, and makes it obvious at a glance if something's missing. The description suffix should be enough that someone reading just the filename knows what it shows (`03-client-marked-footer.jpeg`, not `img3.jpeg`).

Reference images from the HTML with plain relative paths (`<img src="images/03-client-marked-footer.jpeg">`) — not base64. Keeping images as real files means the folder stays inspectable and editable after the fact, and it's the only reason a folder-of-evidence structure makes sense in the first place. (If the user actually wants a single shareable link instead of a local folder, that's a different tool — see the frontmatter note above.)

## Workflow

### 1. Scope the evidence

Before creating anything, work out what evidence already exists as real files (screenshots the user sent, PDFs already on disk) versus what needs to be generated (rendering a PDF page, capturing a live UI state). This shapes the whole task — don't start writing HTML until you know where every image is coming from.

### 2. Create the folder structure first

Make `<report-name>/images/` before writing a line of HTML. Writing the report around images that don't exist yet is how placeholder shortcuts creep in.

### 3. Gather genuine images

- **User-provided files** — copy them into `images/` directly. Never regenerate, re-crop, or "clean up" something the user already gave you as evidence; copy it as-is and reference the copy.
- **PDF evidence** — convert actual pages to images rather than screenshotting a PDF viewer window. `pdftoppm` (poppler) is the most reliable option when available:
  ```
  pdftoppm -png -r 150 -singlefile <input.pdf> <output-basename>
  ```
  Check what's actually installed before picking a tool — availability varies by machine:
  1. `pdftoppm` (`which pdftoppm`) — best quality/control, use if present.
  2. `sips` (macOS built-in) — fallback if poppler isn't installed.
  3. `qlmanage -t` (macOS Quick Look thumbnail) — lower quality, last-resort macOS fallback.
  4. Python `fitz` (PyMuPDF) or `pdf2image` (needs poppler under the hood) — check with a quick `import` before relying on it.

  150 DPI is a reasonable default for a document meant to be read on screen — bump it if the source has small text that needs to stay legible.
- **Live-app / UI evidence** — drive whatever real browser automation is available (Chrome extension tooling, a preview browser pane, etc.) to capture the actual rendered state. The goal is a screenshot of something that really rendered, not a hand-drawn approximation of what it probably looks like.

Whichever source, **read each image back immediately after creating it** (with your Read/image-viewing tool) before moving to the next one. Confirm it shows what you think it shows. Generating five images back-to-back and hoping they're all correct is exactly the kind of shortcut that produces a report you haven't actually verified.

### 4. Build report.html

Start from `assets/template.html` in this skill — it's a theme-aware (light/dark), responsive HTML+CSS shell with the components a report like this typically needs: a title header with status chips, status-bar cards, a quote-thread block for chat/message evidence, figure/figcaption image blocks (single and side-by-side grid), callout boxes (bug / fix / note), and a commit-reference table. Copy it into the report folder, strip out what you don't need, and fill in the rest — you don't need to reinvent the CSS each time, but do treat the content sections as a starting point, not a rigid mold. A report that's mostly prose and one image doesn't need the quote-thread or commit-table sections; use what the actual content calls for.

Every `<img>` should have a caption explaining what it shows and, where relevant, why it's meaningful evidence (not just "screenshot 3" — "the client's original complaint, circled where the field is missing").

### 5. Verify before calling it done

A report isn't finished when the HTML file is written — it's finished when you've confirmed every image actually renders. Don't assume; check.

The reliable, environment-independent check is JavaScript, run against the loaded page:

```js
Array.from(document.querySelectorAll('img')).map(img => ({
  src: img.getAttribute('src'),
  ok: img.complete && img.naturalWidth > 0
}))
```

Every entry should come back `ok: true`. If anything is `false`, the path is wrong or the file is missing or corrupt — fix it and re-check, don't ship it.

**Known gotcha:** some browser preview panes block screenshot capture of local `file://` origins for sandboxing reasons, even though DOM/JavaScript access works completely normally. If a screenshot of your report comes back suspiciously blank or solid black, that's very likely this — not evidence your images are actually broken. Don't conclude the report is broken from a blank screenshot alone; cross-check with the JS snippet above. If you want an actual visual look (not just the programmatic check), sidestep the restriction by serving the folder over a throwaway local HTTP server instead of opening it via `file://`:

```
python3 -m http.server <port>   # run from inside the report folder, in the background
```

then view `http://localhost:<port>/report.html` in the browser tooling you have. Kill the server once you're done looking.

Only report the task as complete once the JS check (and ideally a visual look) both confirm every image is genuinely there and rendering.

### 6. Hand it back

Tell the user the folder path. That's the deliverable — not a prose recap of what's inside it. If there's something worth flagging (an image you couldn't get, a pre-existing issue you noticed but didn't fix), say so explicitly rather than letting it hide in the report.
