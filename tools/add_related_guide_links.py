#!/usr/bin/env python3
"""Add crawlable, topic-related internal links to the published guide set."""

from __future__ import annotations

from html import escape
from html.parser import HTMLParser
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
GROUPS = {
    "connectivity": [
        "guide-1", "guide-2", "guide-3", "guide-4", "usb-ethernet-adapter",
        "usb-c-displayport-adapter", "hdmi-cable", "displayport-cable",
        "usb-peripheral-switch", "kvm-switch", "usb-wifi-adapter",
        "usb-bluetooth-adapter",
    ],
    "storage": [
        "guide-6", "guide-7", "usb-flash-drive-format", "sd-card-reader",
        "external-dvd-drive", "external-backup-drive", "printer-connection",
    ],
    "input": [
        "guide-8", "ergonomic-keyboard", "japanese-keyboard-layout",
        "numeric-keypad", "trackball-mouse", "vertical-mouse", "wrist-rest",
        "mouse-pad", "usb-foot-pedal",
    ],
    "display": [
        "guide-5", "guide-9", "guide-10", "monitor-privacy-filter",
        "monitor-riser", "laptop-stand", "webcam-mount", "webcam-lighting",
        "webcam-privacy-shutter", "desk-task-light",
    ],
    "audio": [
        "guide-9", "usb-microphone", "pc-speakers", "wired-headset",
        "bluetooth-headset", "usb-speakerphone",
    ],
    "workspace": [
        "guide-5", "laptop-stand", "laptop-sleeve", "laptop-backpack",
        "desk-cable-clips", "under-desk-cable-tray", "document-holder",
        "footrest", "desk-task-light", "monitor-riser",
    ],
    "usb-devices": [
        "guide-1", "guide-2", "guide-3", "guide-4", "usb-ethernet-adapter",
        "usb-c-displayport-adapter", "usb-peripheral-switch", "usb-wifi-adapter",
        "usb-bluetooth-adapter", "usb-power-bank", "usb-foot-pedal",
    ],
}


class TitleParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_h1 = False
        self.title = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "h1":
            self.in_h1 = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "h1":
            self.in_h1 = False

    def handle_data(self, data: str) -> None:
        if self.in_h1:
            self.title += data


def main() -> int:
    pages = {p.stem: p for p in SITE.glob("*.html") if p.stem in {slug for group in GROUPS.values() for slug in group}}
    missing = sorted({slug for group in GROUPS.values() for slug in group} - pages.keys())
    if missing:
        raise SystemExit(f"Missing guide pages: {', '.join(missing)}")

    titles: dict[str, str] = {}
    for slug, page in pages.items():
        parser = TitleParser()
        parser.feed(page.read_text(encoding="utf-8"))
        titles[slug] = parser.title.strip()
        if not titles[slug]:
            raise SystemExit(f"Missing h1 in {page.name}")

    changed = 0
    for slug, page in pages.items():
        source = page.read_text(encoding="utf-8")
        group = next(group for group in GROUPS.values() if slug in group)
        index = group.index(slug)
        related = [group[(index + offset) % len(group)] for offset in range(1, min(4, len(group)))]
        links = "".join(
            f'<li><a href="{escape(target)}.html">{escape(titles[target])}</a></li>'
            for target in related
        )
        section = (
            '<section class="related-guides" aria-labelledby="related-guides-title">'
            '<h2 id="related-guides-title">あわせて確認できる購入前ガイド</h2>'
            '<nav aria-label="関連する購入前ガイド"><ul>'
            f"{links}</ul></nav></section>"
        )
        if 'class="related-guides"' in source:
            source = re.sub(
                r'<section class="related-guides".*?</section>',
                section,
                source,
                count=1,
                flags=re.DOTALL,
            )
        else:
            anchor = '<div class="affiliate-cta">'
            if anchor not in source:
                raise SystemExit(f"Affiliate CTA insertion point missing in {page.name}")
            source = source.replace(anchor, section + anchor, 1)
        page.write_text(source, encoding="utf-8", newline="\n")
        changed += 1
    print(f"Added topic-related internal links to {changed} guides.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
