---
title: Docs authoring guide
description: How to write and structure docs for signal-client using MkDocs + Material.
---

# Docs authoring guide

> Tagline: **Async Python framework for resilient Signal bots (community SDK, not the official Signal app).**

## Brand voice
- Audience: Python developers building Signal bots on `signal-cli-rest-api`.
- Positioning: community, async-first bot runtime with resilient ingestion and typed helpers; **not** an official Signal client.
- Tone: practical, concise, confident. Lead with the problem solved; avoid hype.
- Word bank: async, resilient, backpressure, typed, bot runtime, Signal bot, open source, production-minded.
- Avoid: “official Signal client,” “sealed/enterprise,” “magic,” “webhook-only,” “unsupported hacks.”

## Writing guidelines
- Prefer short sentences and bullets for setup steps.
- Name `signal-cli-rest-api` explicitly when relevant; link to upstream project.
- Mention safety defaults (PII redaction on, backpressure) early.
- Invite contributions with clear next actions (issues, PRs, docs edits).

## Page structure
- Start with a single-paragraph summary and a quick “When to use” block.
- Keep headings parallel; include task lists where readers act.
- Add `status`/`note`/`warning` admonitions for risk or prerequisites.
- Use tabs for alternative flows (e.g., Docker vs local).
- Keep examples runnable; prefer copied code blocks over screenshots.

## Components you can use
- Admonitions: `!!! note`, `!!! warning`, `!!! info`.
- Tabs: `=== "Python"` / `=== "CLI"`.
- Cards/grids: `== Example cards` block.
- Diagrams: ```mermaid``` fences for flows; PlantUML optional via remote server toggle.
- Media: Lightbox via Markdown images; avoid autoplay video.
- API references: `::: signal_client` directives render docstrings with source links.

## File conventions
- Add front matter `title`/`description` for SEO and feeds.
- Keep slugs stable; if paths change, add an entry to `redirects` in `mkdocs.yml`.
- Place assets under `docs/assets/` or `assets/` with descriptive names.

## Voice checks
- New landing/intro pages must include the tagline and the community/non-official disclaimer.
- If you add marketing copy, keep it under 40 words and tie it to a concrete capability or safety property.

## Current structure (inventory)
- Overview: `index.md`, `getting_started.md`, `examples.md`, `changelog/`
- Guides: `guides/advanced_usage.md`, `guides/production_deployment.md`, `guides/release.md`
- Reference: `reference/api.md`
- Components: `components/playground.md`
- Docs ops: `contributing/docs-authoring.md`, `contributing/docs-ops.md`
- Repo README: landing hero + disclaimer; mirror the tagline here when updating.
