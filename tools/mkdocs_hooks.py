"""MkDocs hooks used for build-time defaults."""

from __future__ import annotations

import os

from mkdocs.config.defaults import MkDocsConfig


def on_config(config: MkDocsConfig, **_: object) -> MkDocsConfig:
    """Inject environment-controlled analytics toggles and keep strict defaults."""
    analytics_id = os.getenv("MKDOCS_GA4_ID", "").strip()
    if analytics_id:
        config.extra.setdefault("analytics", {})["property"] = analytics_id
    elif "analytics" in config.extra:
        # Ensure analytics are disabled when no ID is provided.
        config.extra["analytics"]["property"] = ""
    return config
