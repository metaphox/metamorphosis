from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import re
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parent.parent
site = root / "_site"


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.posts = []
        self.assets = []
        self.zhihu_images = 0
        self.viewport = None
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "meta" and attrs.get("name") == "viewport":
            self.viewport = attrs.get("content")
        assert attrs.get("id") not in {"existentials", "blogroll"}, "Removed footer section returned"
        if tag == "img":
            assert "data-actualsrc" not in attrs, "Image still requires the old lazy loader"
            src = attrs.get("src", "")
            assert "whitedot.jpg" not in src, "Zhihu placeholder image remains"
            if urlparse(src).hostname and urlparse(src).hostname.endswith(".zhimg.com"):
                assert src.startswith("https://"), "Zhihu image should use HTTPS"
                assert attrs.get("loading") == "lazy", "Missing native lazy loading"
                assert attrs.get("referrerpolicy") == "no-referrer", "Missing hotlink protection fix"
                self.zhihu_images += 1
        if tag == "a":
            assert urlparse(attrs.get("href", "")).hostname != "link.zhihu.com", "Zhihu redirect link remains"
            if attrs.get("class") == "entrylink":
                self.posts.append(attrs["href"])
        if tag in {"link", "script", "img"}:
            url = attrs.get("src", attrs.get("href", ""))
            if url.startswith("/") and not url.startswith("//"):
                self.assets.append(url)


homepage = Page(site / "index.html")
assert homepage.viewport == "width=device-width, initial-scale=1", "Missing mobile viewport"
expected = {
    "/post/" + re.sub(r"^\d{4}-\d{1,2}-\d{1,2}-", "", post.stem) + "/"
    for post in (root / "_posts").iterdir()
}
assert len(homepage.posts) == len(expected), "Post count changed during the build"
assert set(homepage.posts) == expected, "Existing post URLs changed"
assert len(list((site / "post").glob("*/index.html"))) == len(expected)

zhihu_images = 0
for url in homepage.posts:
    page = site / url.lstrip("/") / "index.html"
    assert page.is_file(), f"Missing post: {url}"
    assert "<article>" in page.read_text(), f"Missing post layout: {url}"
    parsed = Page(page)
    assert parsed.viewport == homepage.viewport, f"Missing mobile viewport: {url}"
    zhihu_images += parsed.zhihu_images
    for asset in parsed.assets:
        assert (site / asset.lstrip("/")).is_file(), f"Missing asset: {asset}"

assert zhihu_images == 260, "Imported Zhihu images were lost or duplicated"

for asset in homepage.assets:
    assert (site / asset.lstrip("/")).is_file(), f"Missing asset: {asset}"

css_path = site / "css/screen.css"
css = css_path.read_text()
assert "@use" not in css and not re.search(r"\$[\w-]+", css), "Sass was not compiled"
for url in re.findall(r"url\(([^)]+)\)", css):
    url = url.strip("\"'")
    assert (css_path.parent / url).is_file(), f"Missing CSS image: {url}"

feed = ET.parse(site / "feed.rss")
items = feed.findall("./channel/item")
assert len(items) == 10, "RSS should contain the ten latest posts"
assert [urlparse(item.findtext("link")).path for item in items] == homepage.posts[:10]
assert [urlparse(item.findtext("guid")).path for item in items] == [
    url.rstrip("/") for url in homepage.posts[:10]
], "Existing RSS identifiers changed"
assert all(item.findtext("description") for item in items), "RSS content is empty"
assert (site / "404.html").is_file()
assert Page(site / "404.html").viewport == homepage.viewport, "Missing 404 mobile viewport"
assert not any((site / name).exists() for name in [
    "js", "sass", "resource", "test", "config.ru", "Gemfile", "Gemfile.lock",
    "package.json", "package-lock.json", "node_modules", "wrangler.jsonc",
])
assert not list(site.rglob("*.log")), "Build logs must not be published"
print(f"Checked {len(expected)} posts, {zhihu_images} Zhihu images, preserved URLs, assets, compiled Sass, and RSS.")
