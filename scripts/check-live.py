import concurrent.futures
import urllib.request
from urllib.parse import urljoin, urlsplit, urldefrag
from html.parser import HTMLParser

origin = "https://www.jmbetonservice.nl/"
host = urlsplit(origin).hostname
class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = set()
        self.assets = set()
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self.links.add(a["href"])
        if tag == "link" and a.get("href") and set(a.get("rel","").split()) & {"stylesheet","icon","modulepreload","preload"}:
            self.assets.add(a["href"])
        if tag in {"img","script","source"} and a.get("src"):
            self.assets.add(a["src"])
        if tag in {"img","source"} and a.get("srcset"):
            self.assets.update(x.strip().split()[0] for x in a["srcset"].split(",") if x.strip())

def local(base, value):
    u = urldefrag(urljoin(base, value))[0]
    p = urlsplit(u)
    return u if p.scheme == "https" and p.hostname == host else None

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent":"JM-live-QA/1.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        if r.status != 200:
            raise RuntimeError(f"{url}: HTTP {r.status}")
        return r.url, r.headers.get_content_type(), r.read()

def asset(url):
    final, kind, data = get(url)
    if not data or kind == "text/html":
        raise RuntimeError(f"{url}: invalid asset ({kind})")
    print(f"ASSET OK {kind} {url}")

pending = [origin, urljoin(origin,"contact/"), urljoin(origin,"privacy/")]
seen = set()
assets = set()
while pending:
    url = pending.pop()
    if url in seen:
        continue
    seen.add(url)
    final, kind, data = get(url)
    if kind != "text/html":
        raise RuntimeError(f"{url}: expected HTML, got {kind}")
    page = Page()
    page.feed(data.decode("utf-8"))
    if not any(".css" in x for x in page.assets):
        raise RuntimeError(f"{url}: no stylesheet reference")
    for x in page.assets:
        if (u := local(final,x)):
            assets.add(u)
    for x in page.links:
        if (u := local(final,x)) and u not in seen:
            if urlsplit(u).path.endswith("/") or "." not in urlsplit(u).path.rsplit("/",1)[-1]:
                pending.append(u)
    print(f"PAGE OK {url}")
    if len(seen) > 100:
        raise RuntimeError("Unexpected number of routes")
if len(seen) < 3 or not assets:
    raise RuntimeError("Insufficient page or asset coverage")
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
    list(pool.map(asset, sorted(assets)))
final, kind, data = get("https://jmbetonservice.nl/")
if urlsplit(final).hostname != host:
    raise RuntimeError(f"Apex domain did not redirect to www: {final}")
print(f"LIVE PASS: {len(seen)} pages, {len(assets)} assets, HTTPS and apex redirect")
