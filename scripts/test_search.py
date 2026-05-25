"""Test Steam store suggest HTML parsing."""
import httpx
from html.parser import HTMLParser


class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.results = []
        self.in_name = False
        self.current = {}

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "a" and "data-ds-appid" in d:
            self.current = {"appid": d["data-ds-appid"], "name": "", "url": d.get("href", "")}
        if tag == "div" and d.get("class") == "match_name":
            self.in_name = True

    def handle_data(self, data):
        if self.in_name:
            self.current["name"] = data.strip()
            self.in_name = False
            if self.current:
                self.results.append(self.current)
                self.current = {}


headers = {"User-Agent": "Mozilla/5.0"}
r = httpx.get(
    "https://store.steampowered.com/search/suggest",
    params={"term": "Godot", "f": "games", "cc": "US", "l": "en"},
    headers=headers,
)
print(f"Suggest endpoint: {r.status_code}")
if r.status_code == 200:
    p = Parser()
    p.feed(r.text)
    print(f"Parsed {len(p.results)} results:")
    for res in p.results[:5]:
        print(f'  - {res["name"]} (appid: {res["appid"]})')
