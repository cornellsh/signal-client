---
title: Docs authoring guide
description: How to write and structure docs for signal-client with Material features, macros, and snippets.
---

# Docs authoring guide

> Tagline: **Async Python framework for resilient Signal bots (community SDK, not the official Signal app).**

Use this guide when editing docs so pages stay consistent and on-brand.

## Brand voice

- Audience: Python developers building Signal bots on `signal-cli-rest-api`.
- Positioning: community, async-first bot runtime with resilient ingestion and typed helpers; **not** an official Signal client.
- Tone: practical, concise, confident. Lead with the problem solved; avoid hype.
- Word bank: async, resilient, backpressure, typed, bot runtime, Signal bot, open source, production-minded.
- Avoid: “official Signal client,” “sealed/enterprise,” “magic,” “webhook-only,” “unsupported hacks.”

## Page structure template

Every first-level page should include: front matter (`title`, `description`), a lead/CTA, prerequisites (if applicable), at least one runnable snippet, a diagram for flows, troubleshooting, and “Next steps”. Use [Overview](../index.md) and [Getting started](../getting_started.md) as references.

## Macros & snippets

- Buttons: `{{ cta("Get started", "getting_started.md") }}` renders a Material-styled button.
- Badges: `{{ badge("Beta") }}` or `{{ badge("Experimental", "experimental") }}`.
- Env block: reuse `{{ env_block() }}` instead of duplicating exports.
- Pull code from the repo using `pymdownx.snippets`:

  ```markdown
  ```python
  --8<-- "examples/ping_bot.py"
  ```
  ```
- See live output in [Components playground](../components/playground.md).

## Annotated code

Describe important steps with a short bullet list aligned to each snippet instead of relying on automatic callouts:

```python
@command("!ping")
async def ping(ctx):
    await ctx.reply_text("pong")
```

- Summaries live immediately after the code block.
- Keep explanations concise and focused on what each highlighted action does.

## Tabs, cards, and grids

- Tabs: use `=== "Tab"` blocks for alternative flows (e.g., pip vs Poetry).
- Cards/grids: wrap content in `<div class="brand-grid">` + `<div class="brand-card">` for a consistent layout.

## Media and diagrams

- Diagrams: prefer Mermaid fenced blocks (` ```mermaid `). Keep flows short and legible.
- Images: Markdown images gain a lightbox automatically; add `data-gallery="assets"` when grouping screenshots.
- Icons: use Material icons (`:material-rocket:`) sparingly to anchor cards.

## Cross-linking

- Use relative links; `autorefs` resolves headings automatically. Example: `[Advanced usage](../guides/advanced_usage.md)`.
- When moving content, add redirects in `mkdocs.yml` under `redirect_maps`.

## Voice checks

- Mention the community/non-official disclaimer on landing pages and marketing copy.
- Lead with capability + safety: backpressure, DLQ, redaction.
- Invite contributions with clear next actions (issues, PRs, docs edits).

## Playground

Preview all components on [Components playground](../components/playground.md) before rolling them into guides.
