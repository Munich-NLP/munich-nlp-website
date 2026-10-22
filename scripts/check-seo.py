"""Check the generated site's public URLs and indexing metadata before deploy."""

import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree


class Head(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonicals = []
        self.descriptions = []
        self.robots = ""
        self.redirect = False
        self.in_json = False
        self.json_text = ""
        self.graphs = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonicals.append(attrs.get("href"))
        if tag == "meta":
            if attrs.get("name") == "description":
                self.descriptions.append(attrs.get("content"))
            if attrs.get("name") == "robots":
                self.robots = attrs.get("content", "")
            if attrs.get("http-equiv", "").lower() == "refresh":
                self.redirect = True
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self.in_json = True
            self.json_text = ""

    def handle_data(self, text):
        if self.in_json:
            self.json_text += text

    def handle_endtag(self, tag):
        if tag == "script" and self.in_json:
            self.graphs.append(json.loads(self.json_text))
            self.in_json = False


def check(directory):
    root = Path(directory)
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    sitemap = ElementTree.parse(root / "sitemap.xml")
    urls = [node.text for node in sitemap.findall("s:url/s:loc", ns)]
    assert len(urls) >= 4 and len(urls) == len(set(urls)), "Empty or duplicate sitemap"
    for url in urls:
        parsed = urlsplit(url)
        assert parsed.scheme == "https" and parsed.netloc == "munich-nlp.com", url
        assert not parsed.path.startswith("/home/"), f"Internal content in sitemap: {url}"
        page = root / unquote(parsed.path).lstrip("/") / "index.html"
        assert page.is_file(), f"Sitemap page is missing: {url}"
    indexed = set()
    for page in root.rglob("*.html"):
        head = Head()
        head.feed(page.read_text())
        if head.redirect:
            continue  # Hugo aliases have their own redirect document.
        assert len(head.canonicals) == 1, f"Canonical missing or duplicated: {page}"
        canonical = head.canonicals[0]
        assert canonical.startswith("https://munich-nlp.com/"), canonical
        assert len(head.descriptions) == 1 and head.descriptions[0], page
        assert head.graphs, f"Structured data missing: {page}"
        if "noindex" in head.robots:
            assert canonical not in urls, f"Noindex page in sitemap: {canonical}"
        else:
            assert canonical in urls, f"Public page missing from sitemap: {canonical}"
            indexed.add(canonical)
    assert indexed == set(urls), "Sitemap and public HTML disagree"
    robots = (root / "robots.txt").read_text()
    assert "Sitemap: https://munich-nlp.com/sitemap.xml" in robots
    print(f"SEO checks passed: {len(indexed)} public HTTPS pages, valid metadata and JSON-LD.")


if __name__ == "__main__":
    check(sys.argv[1] if len(sys.argv) > 1 else "public")
