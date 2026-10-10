#!/usr/bin/env python3
"""Turn generic guide checklists into accessible, article-specific SVG diagrams."""

from __future__ import annotations

from html import escape
from html.parser import HTMLParser
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
ASSET_DIR = SITE / "assets" / "guide-visuals"


class GuideParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.in_h1 = False
        self.in_checklist = False
        self.checklist_depth = 0
        self.in_li = False
        self.current_item: list[str] = []
        self.items: list[str] = []
        self.generic_figure = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        if tag == "h1":
            self.in_h1 = True
        if tag == "section" and "purchase-checklist" in (attrs_dict.get("class") or "").split():
            self.in_checklist = True
            self.checklist_depth = 1
        elif self.in_checklist and tag == "section":
            self.checklist_depth += 1
        if tag == "li" and self.in_checklist:
            self.in_li = True
            self.current_item = []
        if tag == "div" and "check-diagram" in (attrs_dict.get("class") or "").split():
            self.generic_figure = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "h1":
            self.in_h1 = False
        if tag == "li" and self.in_li:
            value = "".join(self.current_item).strip()
            if value:
                self.items.append(value)
            self.in_li = False
        if tag == "section" and self.in_checklist:
            self.checklist_depth -= 1
            if self.checklist_depth == 0:
                self.in_checklist = False

    def handle_data(self, data: str) -> None:
        if self.in_h1:
            self.title += data
        if self.in_li:
            self.current_item.append(data)


def wrap_japanese(text: str, limit: int = 14) -> list[str]:
    """Wrap at a readable width, treating East Asian characters as full width."""
    lines: list[str] = []
    current = ""
    width = 0
    for char in text:
        char_width = 2 if ord(char) > 0x2E7F else 1
        if current and width + char_width > limit * 2:
            lines.append(current)
            current = ""
            width = 0
        current += char
        width += char_width
    if current:
        lines.append(current)
    return lines or [text]


def card(item: str, index: int, x: int, width: int, font_size: int) -> str:
    lines = wrap_japanese(item, limit=max(7, (width - 38) // font_size))
    line_step = font_size + 8
    first_line_y = 224 - (len(lines) - 1) * line_step // 2
    text = "".join(
        f'<tspan x="{x + width // 2}" dy="{0 if line_index == 0 else line_step}">{escape(line)}</tspan>'
        for line_index, line in enumerate(lines[:4])
    )
    circle_x = x + min(34, width // 5)
    label_x = circle_x + 30
    return f'''<g>
  <rect x="{x}" y="94" width="{width}" height="274" rx="22" fill="#ffffff" stroke="#d8e5ed" stroke-width="2"/>
  <circle cx="{circle_x}" cy="136" r="19" fill="#173e59"/>
  <text x="{circle_x}" y="142" text-anchor="middle" class="number">{index}</text>
  <text x="{label_x}" y="141" class="step" font-size="{min(15, font_size)}">確認ポイント</text>
  <path d="M{x + 16} 173h{width - 32}" stroke="#e6eef3" stroke-width="2"/>
  <text x="{x + width // 2}" y="{first_line_y}" text-anchor="middle" class="item" font-size="{font_size}">{text}</text>
  <circle cx="{x + width // 2 - 16}" cy="326" r="5" fill="#2b7a78"/>
  <circle cx="{x + width // 2}" cy="326" r="5" fill="#78a9a1"/>
  <circle cx="{x + width // 2 + 16}" cy="326" r="5" fill="#b7d2ce"/>
</g>'''


def render_svg(title: str, items: list[str]) -> str:
    title_xml = escape(title)
    description = escape("購入前に確認する項目: " + "、".join(items))
    count = len(items)
    gap = {3: 40, 4: 24, 5: 16}[count]
    width = (1080 - 40 - gap * (count - 1)) // count
    font_size = {3: 18, 4: 16, 5: 14}[count]
    positions = [20 + index * (width + gap) for index in range(count)]
    cards = "\n".join(card(item, index, x, width, font_size) for index, (item, x) in enumerate(zip(items, positions), 1))
    arrows = "\n".join(
        f'<path d="M{x + width + 4} 231h{gap - 8}m-8-7 8 7-8 7"/>'
        for x in positions[:-1]
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 420" role="img" aria-labelledby="title desc">
<title id="title">{title_xml} — 購入前チェック図</title>
<desc id="desc">{description}</desc>
<defs><linearGradient id="bg" x1="0" x2="1" y1="0" y2="1"><stop stop-color="#f3f9fb"/><stop offset="1" stop-color="#edf4f8"/></linearGradient></defs>
<rect width="1080" height="420" rx="26" fill="url(#bg)"/>
<text x="32" y="56" class="heading">購入前の確認ポイント</text>
<text x="1048" y="55" class="subheading" text-anchor="end">CHECKLIST · {count} ITEMS</text>
{cards}
<g fill="none" stroke="#2b7a78" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
 {arrows}
</g>
<text x="32" y="402" class="footnote">記事内の「購入前の確認メモ」を図に整理しています。条件の詳細は本文と出典をご確認ください。</text>
<style>
 text{{font-family:system-ui,'Meiryo',sans-serif;fill:#172c3f}}
 .heading{{font-size:27px;font-weight:750;letter-spacing:.02em}}
 .subheading{{font-size:12px;font-weight:700;letter-spacing:.16em;fill:#397988}}
 .number{{font-size:16px;font-weight:750;fill:#ffffff}}
 .step{{font-size:15px;font-weight:700;fill:#397988}}
 .item{{font-size:19px;font-weight:700}}
 .footnote{{font-size:13px;fill:#536879}}
</style>
</svg>
'''


def render_mobile_svg(title: str, items: list[str]) -> str:
    title_xml = escape(title)
    description = escape("購入前に確認する項目: " + "、".join(items))
    card_height = 106
    card_gap = 12
    first_y = 86
    canvas_height = first_y + len(items) * card_height + (len(items) - 1) * card_gap + 62
    groups: list[str] = []
    for index, item in enumerate(items, 1):
        y = first_y + (index - 1) * (card_height + card_gap)
        lines = wrap_japanese(item, limit=24)
        line_step = 25
        first_line_y = y + 55 - (len(lines) - 1) * line_step // 2
        text = "".join(
            f'<tspan x="116" dy="{0 if line_index == 0 else line_step}">{escape(line)}</tspan>'
            for line_index, line in enumerate(lines[:3])
        )
        groups.append(f'''<g>
 <rect x="20" y="{y}" width="600" height="{card_height}" rx="18" fill="#ffffff" stroke="#d8e5ed" stroke-width="2"/>
 <circle cx="66" cy="{y + 53}" r="22" fill="#173e59"/>
 <text x="66" y="{y + 59}" text-anchor="middle" class="number">{index}</text>
 <text x="116" y="{first_line_y}" class="item">{text}</text>
</g>''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 {canvas_height}" role="img" aria-labelledby="title desc">
<title id="title">{title_xml} — 購入前チェック図</title>
<desc id="desc">{description}</desc>
<defs><linearGradient id="bg" x1="0" x2="1" y1="0" y2="1"><stop stop-color="#f3f9fb"/><stop offset="1" stop-color="#edf4f8"/></linearGradient></defs>
<rect width="640" height="{canvas_height}" rx="24" fill="url(#bg)"/>
<text x="28" y="52" class="heading">購入前の確認ポイント</text>
{''.join(groups)}
<text x="28" y="{canvas_height - 20}" class="footnote">本文の確認メモを図に整理しています。詳しい条件は記事と出典をご確認ください。</text>
<style>
 text{{font-family:system-ui,'Meiryo',sans-serif;fill:#172c3f}}
 .heading{{font-size:26px;font-weight:750;letter-spacing:.02em}}
 .number{{font-size:16px;font-weight:750;fill:#ffffff}}
 .item{{font-size:20px;font-weight:700}}
 .footnote{{font-size:13px;fill:#536879}}
</style>
</svg>
'''


def main() -> int:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    changed = 0
    for page in sorted(SITE.glob("*.html")):
        if page.name == "index.html" or page.name.startswith("google"):
            continue
        source = page.read_text(encoding="utf-8")
        parsed = GuideParser()
        parsed.feed(source)
        asset = ASSET_DIR / f"{page.stem}.svg"
        mobile_asset = ASSET_DIR / f"{page.stem}-mobile.svg"
        if not parsed.generic_figure and not asset.exists():
            continue
        if len(parsed.items) not in (3, 4, 5):
            raise ValueError(f"Expected 3-5 checklist entries in {page.name}, got {len(parsed.items)}")
        asset.write_text(render_svg(parsed.title, parsed.items), encoding="utf-8", newline="\n")
        mobile_asset.write_text(render_mobile_svg(parsed.title, parsed.items), encoding="utf-8", newline="\n")
        alt = escape("購入前の確認ポイント: " + "、".join(parsed.items), quote=True)
        if parsed.generic_figure:
            figure_match = re.search(r'<figure class="article-figure">.*?</figure>', source, re.DOTALL)
            if figure_match is None:
                raise ValueError(f"Generic diagram found without its figure in {page.name}")
            replacement = (
                f'<figure class="article-figure"><picture><source media="(max-width: 650px)" '
                f'srcset="assets/guide-visuals/{page.stem}-mobile.svg"><img src="assets/guide-visuals/{page.stem}.svg" '
                f'alt="{alt}" width="1080" height="420" decoding="async"></picture>'
                '<figcaption>記事内の「購入前の確認メモ」を項目別に整理した図です。'
                '条件の詳細は本文と出典をご確認ください。</figcaption></figure>'
            )
            source = source[:figure_match.start()] + replacement + source[figure_match.end():]
        else:
            source = re.sub(
                rf'(<figure class="article-figure"><img src="assets/guide-visuals/{re.escape(page.stem)}\.svg"[^>]*>)',
                f'<figure class="article-figure"><picture><source media="(max-width: 650px)" '
                f'srcset="assets/guide-visuals/{page.stem}-mobile.svg"><img src="assets/guide-visuals/{page.stem}.svg" '
                f'alt="{alt}" width="1080" height="420" decoding="async"></picture>',
                source,
            )
            source = re.sub(
                r'<figcaption>.*?</figcaption>',
                '<figcaption>記事内の「購入前の確認メモ」を項目別に整理した図です。'
                '条件の詳細は本文と出典をご確認ください。</figcaption>',
                source,
                count=1,
            )
        page.write_text(source, encoding="utf-8", newline="\n")
        changed += 1
    print(f"Updated {changed} guide diagrams; assets are in {ASSET_DIR.relative_to(ROOT)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
