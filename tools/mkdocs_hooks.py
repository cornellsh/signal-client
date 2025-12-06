"""MkDocs hooks used for build-time defaults."""

from __future__ import annotations

import os
from typing import Any, Dict

def on_config(config: Dict[str, Any], **_: Any) -> Dict[str, Any]:
    """Inject environment-controlled analytics toggles and keep strict defaults."""
    analytics_id = os.getenv("MKDOCS_GA4_ID", "").strip()
    if analytics_id:
        config.extra.setdefault("analytics", {})["property"] = analytics_id
    else:
        # Ensure analytics are disabled when no ID is provided.
        if "analytics" in config.extra:
            config.extra["analytics"]["property"] = ""
    return config
