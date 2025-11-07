import os
import re
import xml.etree.ElementTree as etree

from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor

CUSTOM_IMG_PATTERN = (
    r"""~[{]([^\]]*)[}][(]\s*(<)?([^()<>]+)(>)?(?:\s+(["'])(.*?)\5)?\s*[)]"""
)


class InlineExcalidrawProcessor(InlineProcessor):
    def __init__(
        self,
        pattern,
        md,
        svg_only: bool,
        base_dir: str,
    ):
        self.svg_only = svg_only
        self.base_dir = base_dir
        super().__init__(pattern, md)

    def handleMatch(self, m, data):
        title = m.group(1)
        href = m.group(3)
        desc = m.group(6)

        if self.svg_only:
            with open(
                os.path.join(self.base_dir, href.replace(".json", ".svg")),
            ) as f:
                # remove namespace
                z = re.sub(r'\sxmlns="[^"]+"', "", f.read())
                svg = etree.fromstring(z)

            svg.set("xmlns", "http://www.w3.org/2000/svg")

            svg_desc = etree.Element("desc")
            svg_desc.text = desc
            svg.insert(0, svg_desc)

            svg_title = etree.Element("title")
            svg_title.text = title
            svg.insert(0, svg_title)

            return svg, m.start(0), m.end(0)

        html_id = os.path.basename(href)

        wrapper = etree.Element("div")
        wrapper.set("style", "width: 100%")

        div = etree.Element("div")
        div.set("id", html_id)
        div.set("data-scene", href)

        wrapper.append(div)

        el = etree.Element("script")
        el.set("type", "module")
        el.text = f"""window.excalidraw("{html_id}");"""

        wrapper.append(el)

        return wrapper, m.start(0), m.end(0)


class ExcalidrawExtension(Extension):
    # def __init__(self, svg_only: bool = False, base_dir: str = "excalidraw", **kwargs):
    #     self.svg_only = svg_only
    #     self.base_dir = base_dir
    #     super().__init__(**kwargs)
    def __init__(self, **kwargs):
        self.config = {
            "svg_only": [False, "Only load SVG files (build time)"],
            "base_dir": ["excalidraw", "Base directory for excalidraw files"],
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        md.inlinePatterns.register(
            InlineExcalidrawProcessor(
                CUSTOM_IMG_PATTERN,
                md,
                base_dir=self.getConfig("base_dir"),
                svg_only=self.getConfig("svg_only"),
            ),
            "excalidraw",
            200,
        )


# Function to load the extension
def makeExtension(**kwargs):
    return ExcalidrawExtension(**kwargs)
