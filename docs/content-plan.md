# Signal Client Documentation Content Plan

> Tone alignment: mirror the concise, imperative voice of the `signal-cli-rest-api` README—state the what, then the how, with direct user actions and minimal fluff.

- [x] **Finalize theme capabilities reference**
  - [x] Catalog mkdocs-shadcn demonstrations for admonitions, attribute lists, codehilite, codexec, echarts, fenced code, footnotes, iconify, pymdownx blocks, progress bars, tabbed layouts, Excalidraw, and mkdocstrings.
  - [x] Annotate which components are required on each page within this plan once drafts begin.
- [x] **Define editorial guardrails**
  - [x] Document the tone, terminology, and formatting patterns in a shared style snippet.
  - [x] Align call-to-action phrasing with existing README conventions.
  - [x] Produce a short glossary for recurring protocol/library terms.

### Theme Components by Page

| Section | Must-use Components | Optional Enhancements |
| --- | --- | --- |
| Landing Page | Iconify feature grid, details blocks, attr list CTAs | Progress bar (roadmap cameo) |
| Getting Started | Admonitions, tabbed install blocks, codexec snippet, progress bar, footnotes | Iconify inline hints |
| Configuration & Setup | Captioned tables, details blocks, warning/danger admonitions | Excalidraw diagram, attr-list badges |
| Usage Guides | Tabbed multi-language code, codexec (where safe), codehilite samples, numbered lists | Iconify markers, footnotes |
| API Reference | mkdocstrings, admonition callouts | Attribute list badges, footnotes |
| Recipes & Tutorials | Progress bars, details blocks, fenced code, iconify cues | Excalidraw diagrams |
| Diagnostics & Troubleshooting | Details accordions, captioned tables, warning/danger admonitions, footnotes | Progress bars for workflow status |
| Changelog & Roadmap | Iconify badges, progress bar timeline, details blocks | Footnotes for release notes |
| Resources & Community | Captioned tables, attr list link badges, iconify icons, admonition CTA | Footnotes for policies |

### Editorial Guardrails

- **Voice & Structure**: Lead with outcomes (“Register your client”), follow with concise imperative steps. Prefer short paragraphs, avoid marketing superlatives, and keep technical nouns consistent (Signal Client, signal-cli, device link).
- **Formatting**: Use sentence case headings, italicize UI navigation (e.g., *Linked devices*), code for CLI commands, fenced code for multi-line payloads. Reserve bold for key actions or warnings.
- **Call-to-Action Patterns**: Mirror README cadence—`Do X` statement followed by command snippet. Example: “Start the REST bridge, then run:” followed by code block. Hyperlinks should describe the action (“Review device linking guide”) rather than “click here.”
- **Glossary Highlights**:
  - `Primary device`: The mobile Signal account owner.
  - `Linked device`: A secondary client authenticated via device linking flow.
  - `Registration`: Initial number verification for first-time client setup.
  - `Daemon mode`: Long-running process keeping the Signal session active.
  - `Story`: Time-bound broadcast message object in Signal ecosystem.
  - `Attachment handle`: Identifier returned for uploaded media assets.
- **Consistency Hooks**: Reuse admonition titles (`Note`, `Warning`, `Important`) across pages; prefer the same order of sections (Overview → Steps → Verify). Align bullet spacing and avoid inline HTML where Markdown suffices.

## 1. Landing Page

- [x] Draft hero statement and subheading focused on Signal Client value proposition.
- [x] Assemble quick-start call-to-action buttons using `attr_list` for styling.
- [x] Add feature grid with icon bullets via `+iconify+` syntax.
- [x] Insert collapsible “Why Signal Client?” detail block leveraging `pymdownx.blocks.details`.
- [x] Validate dark/light contrast for all highlights.

## 2. Getting Started

- [x] Confirm prerequisites (runtime, OS, dependencies) in a note admonition.
- [x] Provide installation tabs (`pip`, `uv`, `poetry`, `npm`) using `pymdownx.blocks.tab`.
- [x] Embed a codexec-enabled “send first message” snippet for Python.
- [x] Add troubleshooting footnotes for registration hiccups.
- [x] Include a progress bar checklist for first-run milestones.

## 3. Configuration & Setup

- [x] Outline environment variables in a table with `pymdownx.blocks.caption`.
- [x] Supply collapsible sections per deployment mode (CLI, REST, SDK).
- [x] Highlight security-sensitive steps with warning/danger admonitions.
- [x] Document key management flow in an Excalidraw diagram reference.
- [x] Cross-link to diagnostics page via attribute list-styled badges.

## 4. Usage Guides

- [x] Break down messaging, group management, media handling, and webhook workflows into subsections.
- [x] For each capability, add multi-language code tabs (Python/TypeScript) and codexec where safe.
- [x] Insert flow summaries using numbered lists and callout notes.
- [x] Showcase payload/response pairs with fenced code blocks and `codehilite`.
- [x] Add inline icons to emphasize prerequisites or optional enhancements.

## 5. API Reference

- [x] Configure `mkdocstrings` for auto-generated API docs (verify handler options).
- [x] Ensure root headings and cross-reference anchors align with navigation.
- [x] Provide example queries and responses alongside each endpoint summary.
- [x] Add admonition blocks for preview/experimental endpoints.
- [x] Surface `last-updated` info if `show_datetime` is enabled per page.

## 6. Recipes & Tutorials

- [x] Curate at least five scenario-driven guides (e.g., encrypted attachments, broadcast alerts).
- [x] Introduce each recipe with a success metric progress bar.
- [x] Incorporate collapsible “Deep dive” sections with details blocks.
- [x] Attach optional diagrams (Excalidraw) for architecture-heavy tutorials.
- [x] Link to companion scripts in `scripts/` or examples repository.

## 7. Diagnostics & Troubleshooting

- [x] Build FAQ-style accordions via `pymdownx.blocks.details`.
- [x] Document common error codes in a captioned table.
- [x] Provide copy-paste diagnostics commands with fenced code blocks.
- [x] Add danger admonitions for destructive operations.
- [x] Use footnotes for platform-specific caveats.

## 8. Changelog & Roadmap

- [x] Compile release highlights with iconified badges for “New”, “Improved”, “Fixed”.
- [x] Render future milestones as a progress bar timeline.
- [x] Link each entry back to relevant recipe or API sections.
- [x] Add collapsible detail blocks for deprecations.
- [x] Ensure dates respect `show_datetime` configuration.

## 9. Resources & Community

- [x] Aggregate community libraries/tools in a table with caption for quick scan.
- [x] Provide external link badges (API Reference, GitHub, Community forum) using attribute lists.
- [x] Embed iconify icons for channel identification.
- [x] Add footnotes for contribution guidelines or support SLAs.
- [x] Include a “Get involved” callout admonition with CTA links.

## Global QA & Publishing

- [ ] Verify navigation ordering (`order` metadata or filesystem prefixes).
- [ ] Check that all admonition, tab, and codexec features render in both light/dark themes.
- [ ] Run `mkdocs serve` smoke test and review layout responsiveness.
- [ ] Execute link checks and linting (ruff, mypy, pytest) before publish.
- [ ] Coordinate final editorial review and merge workflow.
