from __future__ import annotations

from mkdocs_macros.plugin import MacrosPlugin


def define_env(env: MacrosPlugin) -> None:
    env.variables.update(
        {
            "signal": {
                "package": "signal-client",
                "min_python": "3.11",
                "deployment_targets": "Signal Cloud • Bring Your Own Infrastructure",
            }
        }
    )

    @env.macro
    def spotlight_stat(label: str, value: str) -> str:
        wrapper_style = (
            "display:inline-flex;"
            "align-items:center;"
            "gap:0.5rem;"
            "padding:0.35rem 0.75rem;"
            "border-radius:0.75rem;"
            "border:1px solid rgba(15,23,42,0.15);"
            "background:rgba(15,23,42,0.04);"
            "font-size:0.95rem;"
            "line-height:1.2;"
            "white-space:nowrap"
        )
        label_style = "color:rgba(15,23,42,0.7);font-weight:500"
        value_style = "font-weight:600;color:#0f172a"
        return (
            f'<span style="{wrapper_style};">'
            f'<span style="{label_style};">{label}</span>'
            f'<span style="{value_style};">{value}</span>'
            "</span>"
        )

    @env.macro
    def install_snippet(flavors: str = "pip") -> str:
        command = (
            "pip install signal-client"
            if flavors == "pip"
            else "poetry add signal-client"
        )
        return f"`{command}`"
