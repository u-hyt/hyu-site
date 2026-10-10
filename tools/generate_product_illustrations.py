#!/usr/bin/env python3
"""Add original category illustrations that link to each guide's tagged Amazon search."""

from __future__ import annotations

from html import escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlparse
import re


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
ASSET_DIR = SITE / "assets" / "product-illustrations"

# These are original, generic category drawings. They do not depict Amazon listings.
SYMBOLS = {
    "guide-1": "hub", "guide-2": "cable", "guide-3": "charger", "guide-4": "dock",
    "guide-5": "monitor", "guide-6": "ssd", "guide-7": "sd-card", "guide-8": "keyboard-mouse",
    "guide-9": "webcam", "guide-10": "monitor-arm",
    "usb-ethernet-adapter": "ethernet-adapter", "hdmi-cable": "cable", "usb-c-displayport-adapter": "video-adapter",
    "printer-connection": "printer", "usb-flash-drive-format": "flash-drive", "sd-card-reader": "card-reader",
    "external-dvd-drive": "dvd-drive", "usb-microphone": "microphone", "pc-speakers": "speakers",
    "laptop-stand": "laptop-stand", "ergonomic-keyboard": "keyboard", "japanese-keyboard-layout": "keyboard-jis",
    "numeric-keypad": "keypad", "trackball-mouse": "trackball", "vertical-mouse": "vertical-mouse",
    "wrist-rest": "wrist-rest", "mouse-pad": "mouse-pad", "usb-peripheral-switch": "usb-switch",
    "kvm-switch": "kvm", "displayport-cable": "cable", "monitor-privacy-filter": "privacy-filter",
    "monitor-riser": "monitor-riser", "document-holder": "document-holder", "footrest": "footrest",
    "desk-task-light": "lamp", "laptop-sleeve": "laptop-sleeve", "laptop-backpack": "backpack",
    "desk-cable-clips": "cable-clips", "under-desk-cable-tray": "cable-tray", "wired-headset": "headset",
    "bluetooth-headset": "headset", "usb-speakerphone": "speakerphone", "webcam-privacy-shutter": "webcam-shutter",
    "webcam-lighting": "ring-light", "webcam-mount": "webcam-mount", "external-backup-drive": "ssd",
    "usb-power-bank": "power-bank", "usb-wifi-adapter": "wifi-adapter", "usb-bluetooth-adapter": "bluetooth-adapter",
    "usb-foot-pedal": "foot-pedal",
}


class GuideParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.in_h1 = False
        self.affiliate_href = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "h1":
            self.in_h1 = True
        if tag == "a" and "hyusiteguide-22" in (values.get("href") or ""):
            self.affiliate_href = values["href"] or ""

    def handle_endtag(self, tag: str) -> None:
        if tag == "h1":
            self.in_h1 = False

    def handle_data(self, data: str) -> None:
        if self.in_h1:
            self.title += data


def category_name(title: str) -> str:
    return re.split(r"(?:の選び方|購入前)", title, maxsplit=1)[0].strip(" ：:") or title


def search_label(href: str) -> str:
    params = parse_qs(urlparse(href).query)
    query = params.get("k", params.get("s", [""]))[0]
    return query.strip() or "関連商品"


def drawing(symbol: str) -> str:
    stroke = '#17445f'
    blue = '#2e83ae'
    teal = '#2b7a78'
    gold = '#f1ad58'
    light = '#dcecf1'
    shapes = {
        "flash-drive": f'<rect x="166" y="111" width="210" height="118" rx="28" fill="{blue}"/><path d="M376 139h57v62h-57" fill="{gold}" stroke="{stroke}" stroke-width="8"/><path d="M396 153v33m18-33v33" stroke="{stroke}" stroke-width="7"/><circle cx="207" cy="170" r="9" fill="{gold}"/>',
        "hub": f'<path d="M130 155C91 155 92 209 63 209" fill="none" stroke="{stroke}" stroke-width="16" stroke-linecap="round"/><rect x="132" y="115" width="298" height="112" rx="28" fill="{blue}" stroke="{stroke}" stroke-width="8"/><rect x="186" y="145" width="50" height="20" rx="7" fill="#fff"/><rect x="258" y="145" width="50" height="20" rx="7" fill="#fff"/><rect x="330" y="145" width="50" height="20" rx="7" fill="#fff"/><circle cx="202" cy="194" r="8" fill="{gold}"/>',
        "cable": f'<path d="M143 208C183 77 388 80 421 204" fill="none" stroke="{blue}" stroke-width="22" stroke-linecap="round"/><rect x="110" y="180" width="62" height="49" rx="10" fill="{gold}" stroke="{stroke}" stroke-width="7"/><path d="M119 193h-27v22h27m322-35h29v45h-29" fill="{gold}" stroke="{stroke}" stroke-width="7" stroke-linejoin="round"/>',
        "charger": f'<rect x="188" y="90" width="184" height="155" rx="30" fill="{blue}" stroke="{stroke}" stroke-width="8"/><path d="M236 86V60m91 26V60" stroke="{stroke}" stroke-width="12" stroke-linecap="round"/><rect x="228" y="121" width="45" height="17" rx="7" fill="#fff"/><path d="m300 119-23 42h25l-13 38 45-53h-27l15-27" fill="{gold}"/>',
        "monitor": f'<rect x="118" y="75" width="324" height="187" rx="18" fill="{blue}" stroke="{stroke}" stroke-width="10"/><rect x="143" y="99" width="274" height="135" rx="8" fill="{light}"/><path d="M279 263v39m-70 8h140" stroke="{stroke}" stroke-width="14" stroke-linecap="round"/>',
        "ssd": f'<rect x="155" y="103" width="250" height="150" rx="30" fill="{blue}" stroke="{stroke}" stroke-width="9"/><path d="M405 165h45v28h-45" fill="{gold}" stroke="{stroke}" stroke-width="7"/><circle cx="206" cy="177" r="14" fill="{gold}"/><path d="M248 152h113m-113 22h84" stroke="#dff2f3" stroke-width="9" stroke-linecap="round"/>',
        "sd-card": f'<path d="M186 75h157l60 60v144H186z" fill="{blue}" stroke="{stroke}" stroke-width="9" stroke-linejoin="round"/><path d="M343 75v62h60" fill="{light}" stroke="{stroke}" stroke-width="8"/><path d="M219 100v45m28-45v45m28-45v45m28-45v45" stroke="{gold}" stroke-width="9"/>',
        "keyboard": f'<rect x="74" y="106" width="412" height="154" rx="22" fill="{blue}" stroke="{stroke}" stroke-width="8"/>'+''.join(f'<rect x="{100+col*45}" y="{130+row*34}" width="32" height="21" rx="5" fill="{light}"/>' for row in range(3) for col in range(8))+f'<rect x="210" y="234" width="152" height="12" rx="6" fill="{gold}"/>',
        "keyboard-mouse": f'<rect x="66" y="117" width="292" height="124" rx="18" fill="{blue}" stroke="{stroke}" stroke-width="8"/>'+''.join(f'<rect x="{86+col*38}" y="{136+row*30}" width="27" height="18" rx="4" fill="{light}"/>' for row in range(3) for col in range(6))+f'<path d="M410 121c-35 0-55 29-55 61s20 60 55 60 55-28 55-60-20-61-55-61z" fill="{gold}" stroke="{stroke}" stroke-width="8"/><path d="M410 125v44m-9 0h18" stroke="{stroke}" stroke-width="7"/>',
        "keypad": f'<rect x="190" y="72" width="180" height="228" rx="24" fill="{blue}" stroke="{stroke}" stroke-width="8"/>'+''.join(f'<rect x="{216+(i%3)*45}" y="{98+(i//3)*42}" width="32" height="28" rx="6" fill="{light}"/>' for i in range(12))+f'<rect x="261" y="266" width="77" height="17" rx="7" fill="{gold}"/>',
        "trackball": f'<path d="M152 110q0-34 38-34h180q38 0 38 34v107q0 37-38 37H190q-38 0-38-37z" fill="{blue}" stroke="{stroke}" stroke-width="9"/><circle cx="280" cy="151" r="52" fill="{gold}" stroke="{stroke}" stroke-width="8"/><path d="M280 104v23" stroke="{stroke}" stroke-width="7"/>',
        "vertical-mouse": f'<path d="M214 268c-46-27-67-94-43-151 17-41 54-60 101-58 44 2 76 25 84 66 10 51-12 112-56 143-26 19-58 20-86 0z" fill="{blue}" stroke="{stroke}" stroke-width="9"/><path d="M281 70v91m-38-30q37 18 75 0" fill="none" stroke="{light}" stroke-width="9" stroke-linecap="round"/>',
        "wrist-rest": f'<rect x="100" y="112" width="360" height="54" rx="26" fill="{gold}" stroke="{stroke}" stroke-width="8"/><rect x="75" y="190" width="410" height="74" rx="19" fill="{blue}" stroke="{stroke}" stroke-width="8"/>'+''.join(f'<rect x="{98+(i%9)*42}" y="{205+(i//9)*25}" width="31" height="14" rx="4" fill="{light}"/>' for i in range(18)),
        "mouse-pad": f'<path d="M84 232q4-95 120-130h247q-7 108-126 144H95q-11 0-11-14z" fill="{light}" stroke="{stroke}" stroke-width="8"/><path d="M303 110c-32 0-50 25-50 55s18 52 50 52 50-22 50-52-18-55-50-55z" fill="{gold}" stroke="{stroke}" stroke-width="8"/>',
        "usb-switch": f'<rect x="125" y="126" width="310" height="120" rx="25" fill="{blue}" stroke="{stroke}" stroke-width="8"/><rect x="164" y="162" width="62" height="24" rx="7" fill="#fff"/><rect x="250" y="162" width="62" height="24" rx="7" fill="#fff"/><circle cx="370" cy="181" r="18" fill="{gold}" stroke="{stroke}" stroke-width="6"/><path d="M73 185h51m311 0h51" stroke="{stroke}" stroke-width="10" stroke-linecap="round"/>',
        "kvm": f'<rect x="160" y="126" width="240" height="102" rx="24" fill="{blue}" stroke="{stroke}" stroke-width="8"/><circle cx="223" cy="177" r="14" fill="{gold}"/><circle cx="280" cy="177" r="14" fill="{light}"/><circle cx="337" cy="177" r="14" fill="{light}"/><path d="M166 148 100 103m-4 0h-40m346 45 64-45m0 0h42m-175 125v44" fill="none" stroke="{stroke}" stroke-width="9" stroke-linecap="round"/>',
        "video-adapter": f'<rect x="167" y="132" width="170" height="88" rx="24" fill="{blue}" stroke="{stroke}" stroke-width="8"/><path d="M337 158h68v38h-68" fill="{gold}" stroke="{stroke}" stroke-width="8"/><path d="M192 161h46v29h-46" fill="#fff"/><path d="M166 175h-55" stroke="{stroke}" stroke-width="12"/>',
        "ethernet-adapter": f'<rect x="169" y="139" width="205" height="91" rx="24" fill="{blue}" stroke="{stroke}" stroke-width="8"/><path d="M374 160h72v55h-72" fill="{gold}" stroke="{stroke}" stroke-width="8"/><path d="M394 177h32m-32 14h32m-32 14h32" stroke="{stroke}" stroke-width="5"/><path d="M169 185h-67" stroke="{stroke}" stroke-width="12"/>',
        "wifi-adapter": f'<rect x="192" y="151" width="156" height="69" rx="22" fill="{blue}" stroke="{stroke}" stroke-width="8"/><path d="M192 171h-50v31h50" fill="{gold}" stroke="{stroke}" stroke-width="7"/><path d="M369 142q47 38 0 78m22-100q73 61 0 122" fill="none" stroke="{teal}" stroke-width="10" stroke-linecap="round"/>',
        "bluetooth-adapter": f'<rect x="193" y="154" width="142" height="64" rx="20" fill="{blue}" stroke="{stroke}" stroke-width="8"/><path d="M193 172h-50v29h50" fill="{gold}" stroke="{stroke}" stroke-width="7"/><path d="m365 94 54 48-48 41 48 43-54 45V94m0 90-44-43m44 43-44 42" fill="none" stroke="{teal}" stroke-width="9" stroke-linejoin="round"/>',
        "printer": f'<path d="M176 89h208v74H176z" fill="{light}" stroke="{stroke}" stroke-width="8"/><rect x="106" y="145" width="348" height="130" rx="25" fill="{blue}" stroke="{stroke}" stroke-width="8"/><path d="M165 226h230v66H165z" fill="#fff" stroke="{stroke}" stroke-width="7"/><circle cx="397" cy="184" r="9" fill="{gold}"/>',
        "card-reader": f'<rect x="165" y="130" width="230" height="98" rx="24" fill="{blue}" stroke="{stroke}" stroke-width="8"/><path d="M212 157h76v29h-76z" fill="#fff"/><path d="M318 156h45v34h-45z" fill="{gold}"/><path d="M164 178h-56" stroke="{stroke}" stroke-width="12"/>',
        "dvd-drive": f'<rect x="110" y="112" width="340" height="154" rx="24" fill="{blue}" stroke="{stroke}" stroke-width="8"/><rect x="145" y="145" width="270" height="64" rx="10" fill="#eaf3f5" stroke="{stroke}" stroke-width="5"/><circle cx="280" cy="178" r="26" fill="{gold}" stroke="{stroke}" stroke-width="6"/><circle cx="280" cy="178" r="6" fill="#fff"/>',
        "microphone": f'<rect x="232" y="80" width="96" height="156" rx="47" fill="{blue}" stroke="{stroke}" stroke-width="8"/><path d="M202 167v28q0 67 78 67t78-67v-28m-78 95v33m-56 0h112" fill="none" stroke="{stroke}" stroke-width="10" stroke-linecap="round"/><path d="M250 123h60m-60 25h60" stroke="{light}" stroke-width="8" stroke-linecap="round"/>',
        "speakers": f'<rect x="113" y="90" width="136" height="200" rx="24" fill="{blue}" stroke="{stroke}" stroke-width="8"/><rect x="311" y="90" width="136" height="200" rx="24" fill="{blue}" stroke="{stroke}" stroke-width="8"/><circle cx="181" cy="158" r="34" fill="{light}" stroke="{stroke}" stroke-width="6"/><circle cx="181" cy="238" r="20" fill="{gold}" stroke="{stroke}" stroke-width="6"/><circle cx="379" cy="158" r="34" fill="{light}" stroke="{stroke}" stroke-width="6"/><circle cx="379" cy="238" r="20" fill="{gold}" stroke="{stroke}" stroke-width="6"/>',
        "headset": f'<path d="M158 192v-35q0-119 122-119t122 119v35" fill="none" stroke="{stroke}" stroke-width="20" stroke-linecap="round"/><rect x="137" y="166" width="72" height="118" rx="30" fill="{blue}" stroke="{stroke}" stroke-width="8"/><rect x="351" y="166" width="72" height="118" rx="30" fill="{blue}" stroke="{stroke}" stroke-width="8"/><path d="M350 255q-10 40-67 35" fill="none" stroke="{gold}" stroke-width="10" stroke-linecap="round"/>',
        "speakerphone": f'<circle cx="280" cy="179" r="104" fill="{blue}" stroke="{stroke}" stroke-width="9"/><circle cx="280" cy="179" r="58" fill="{light}" stroke="{stroke}" stroke-width="7"/><circle cx="280" cy="179" r="19" fill="{gold}"/><circle cx="214" cy="252" r="8" fill="#fff"/><circle cx="242" cy="265" r="8" fill="#fff"/><circle cx="272" cy="270" r="8" fill="#fff"/><circle cx="302" cy="265" r="8" fill="#fff"/><circle cx="330" cy="252" r="8" fill="#fff"/>',
        "webcam": f'<rect x="137" y="105" width="286" height="150" rx="26" fill="{blue}" stroke="{stroke}" stroke-width="9"/><circle cx="280" cy="180" r="56" fill="{light}" stroke="{stroke}" stroke-width="8"/><circle cx="280" cy="180" r="28" fill="{gold}" stroke="{stroke}" stroke-width="7"/><path d="M228 258h104m-52 0v37" stroke="{stroke}" stroke-width="9" stroke-linecap="round"/>',
        "webcam-shutter": f'<rect x="137" y="105" width="286" height="150" rx="26" fill="{blue}" stroke="{stroke}" stroke-width="9"/><circle cx="280" cy="180" r="54" fill="{light}" stroke="{stroke}" stroke-width="8"/><circle cx="280" cy="180" r="24" fill="{gold}"/><rect x="250" y="160" width="106" height="39" rx="18" fill="#f7f9fc" fill-opacity=".88" stroke="{stroke}" stroke-width="6"/><path d="M232 258h96m-48 0v35" stroke="{stroke}" stroke-width="9" stroke-linecap="round"/>',
        "ring-light": f'<circle cx="280" cy="164" r="106" fill="none" stroke="{stroke}" stroke-width="19"/><circle cx="280" cy="164" r="78" fill="none" stroke="{gold}" stroke-width="12"/><path d="M280 270v36m-58 0h116" stroke="{stroke}" stroke-width="12" stroke-linecap="round"/><rect x="260" y="142" width="40" height="46" rx="11" fill="{blue}"/>',
        "webcam-mount": f'<rect x="207" y="85" width="146" height="89" rx="22" fill="{blue}" stroke="{stroke}" stroke-width="8"/><circle cx="280" cy="129" r="26" fill="{gold}" stroke="{stroke}" stroke-width="6"/><path d="M280 174v80q0 22-22 22h-65v37h174v-37h-65q-22 0-22-22" fill="none" stroke="{stroke}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>',
        "monitor-arm": f'<rect x="116" y="71" width="208" height="135" rx="14" fill="{blue}" stroke="{stroke}" stroke-width="8"/><path d="M222 207v73l105-1 76-87 22 18" fill="none" stroke="{stroke}" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/><path d="M408 212v57m-35 17h70" stroke="{stroke}" stroke-width="12" stroke-linecap="round"/>',
        "privacy-filter": f'<rect x="126" y="70" width="308" height="184" rx="17" fill="{blue}" stroke="{stroke}" stroke-width="9"/><rect x="150" y="94" width="260" height="136" rx="7" fill="{light}"/><path d="M198 110 158 210m305-95-40 100" stroke="{gold}" stroke-opacity=".8" stroke-width="14"/><path d="M280 254v48m-72 7h144" stroke="{stroke}" stroke-width="12" stroke-linecap="round"/>',
        "monitor-riser": f'<rect x="153" y="71" width="254" height="140" rx="16" fill="{blue}" stroke="{stroke}" stroke-width="8"/><path d="M281 211v42m-132 8h264v40H149z" fill="{gold}" stroke="{stroke}" stroke-width="8" stroke-linejoin="round"/>',
        "document-holder": f'<path d="M151 89h169l89 92v106H151z" fill="#fff" stroke="{stroke}" stroke-width="8"/><path d="M320 89v92h89m-216-49h96m-96 32h150m-150 31h188" stroke="{blue}" stroke-width="9" stroke-linecap="round"/><path d="M129 298h302" stroke="{stroke}" stroke-width="10" stroke-linecap="round"/>',
        "footrest": f'<path d="M120 233q37-104 160-104t160 104H120z" fill="{blue}" stroke="{stroke}" stroke-width="9"/><path d="M146 237h268v46H146z" fill="{gold}" stroke="{stroke}" stroke-width="8"/><path d="M175 283v22m210-22v22" stroke="{stroke}" stroke-width="10" stroke-linecap="round"/>',
        "lamp": f'<path d="M141 109h150l-32 66h-86z" fill="{gold}" stroke="{stroke}" stroke-width="8" stroke-linejoin="round"/><path d="m240 176 93 72m-93-72-44 78m117-6h95" fill="none" stroke="{stroke}" stroke-width="12" stroke-linecap="round"/><path d="M190 278h213" stroke="{blue}" stroke-width="17" stroke-linecap="round"/><path d="M160 187h-33m210-8 27-23m-7 49 39-1" stroke="{gold}" stroke-width="8" stroke-linecap="round"/>',
        "laptop-stand": f'<path d="M130 224h300l-27 31H155z" fill="{gold}" stroke="{stroke}" stroke-width="8" stroke-linejoin="round"/><path d="m194 221 28-87h95l41 87" fill="none" stroke="{stroke}" stroke-width="13" stroke-linejoin="round"/><rect x="177" y="71" width="169" height="114" rx="12" fill="{blue}" stroke="{stroke}" stroke-width="8"/><path d="M280 185v34" stroke="{stroke}" stroke-width="10"/>',
        "laptop-sleeve": f'<rect x="138" y="82" width="284" height="188" rx="28" fill="{blue}" stroke="{stroke}" stroke-width="9"/><path d="M154 114h252v115H154z" fill="{light}"/><path d="M200 244h160" stroke="{gold}" stroke-width="9" stroke-linecap="round"/>',
        "backpack": f'<path d="M178 133q0-60 102-60t102 60l30 157H148z" fill="{blue}" stroke="{stroke}" stroke-width="9"/><path d="M216 131q0-35 64-35t64 35m-146 38h196v76H198z" fill="none" stroke="{light}" stroke-width="9"/><path d="M232 245v32m96-32v32" stroke="{gold}" stroke-width="9" stroke-linecap="round"/>',
        "cable-clips": f'<path d="M126 108c0 100 95 0 95 104s92-94 92 5 95-83 95-7" fill="none" stroke="{blue}" stroke-width="13" stroke-linecap="round"/><path d="M186 155q35-31 67 0v48q-32-30-67 0zm140-14q35-31 67 0v48q-32-30-67 0z" fill="{gold}" stroke="{stroke}" stroke-width="8"/><path d="M110 272h340" stroke="{stroke}" stroke-width="10" stroke-linecap="round"/>',
        "cable-tray": f'<path d="M95 103h370" stroke="{stroke}" stroke-width="15" stroke-linecap="round"/><path d="M134 120v87h293v-87" fill="{blue}" stroke="{stroke}" stroke-width="9" stroke-linejoin="round"/><path d="M160 151h239m-239 27h239" stroke="{light}" stroke-width="10" stroke-linecap="round"/><path d="M200 209v57m160-57v57" stroke="{stroke}" stroke-width="10"/>',
        "power-bank": f'<rect x="191" y="62" width="178" height="240" rx="32" fill="{blue}" stroke="{stroke}" stroke-width="9"/><rect x="231" y="89" width="100" height="14" rx="7" fill="#fff"/><path d="m284 126-32 58h32l-15 48 48-69h-32l16-37" fill="{gold}"/><circle cx="254" cy="273" r="8" fill="#fff"/><circle cx="280" cy="273" r="8" fill="#fff"/><circle cx="306" cy="273" r="8" fill="#fff"/>',
        "dock": f'<rect x="114" y="103" width="332" height="150" rx="26" fill="{blue}" stroke="{stroke}" stroke-width="9"/><path d="M151 141h51v20h-51m78-20h51v20h-51m78-20h51v20h-51" stroke="#fff" stroke-width="8" stroke-linecap="round"/><circle cx="171" cy="201" r="9" fill="{gold}"/><path d="M278 253v42m-68 2h136" stroke="{stroke}" stroke-width="10" stroke-linecap="round"/>',
        "keyboard-jis": f'<rect x="74" y="106" width="412" height="154" rx="22" fill="{blue}" stroke="{stroke}" stroke-width="8"/>'+''.join(f'<rect x="{98+col*38}" y="{129+row*34}" width="28" height="21" rx="5" fill="{light}"/>' for row in range(3) for col in range(9))+f'<rect x="370" y="197" width="83" height="22" rx="5" fill="{gold}"/><rect x="201" y="234" width="150" height="12" rx="6" fill="{gold}"/>',
        "ring-light": f'<circle cx="280" cy="145" r="92" fill="none" stroke="{stroke}" stroke-width="20"/><circle cx="280" cy="145" r="69" fill="none" stroke="{gold}" stroke-width="14"/><rect x="257" y="126" width="46" height="49" rx="11" fill="{blue}"/><path d="M280 239v52m-65 9h130" stroke="{stroke}" stroke-width="12" stroke-linecap="round"/>',
        "foot-pedal": f'<path d="M163 218q19-99 117-99t117 99H163z" fill="{blue}" stroke="{stroke}" stroke-width="9"/><path d="M198 222h164v44H198z" fill="{gold}" stroke="{stroke}" stroke-width="8"/><path d="M223 267v29m114-29v29" stroke="{stroke}" stroke-width="10" stroke-linecap="round"/>',
    }
    return shapes.get(symbol, shapes["hub"])


def render_svg(title: str, category: str, symbol: str) -> str:
    title_xml = escape(title)
    label_xml = escape(category)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 360" role="img" aria-labelledby="title desc">
<title id="title">{title_xml} — {label_xml}のカテゴリイラスト</title>
<desc id="desc">特定の販売商品ではなく、{label_xml}という製品カテゴリを示すオリジナルの説明イラストです。</desc>
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#f4f9fc"/><stop offset="1" stop-color="#e8f2f7"/></linearGradient><filter id="shadow" x="-.2" y="-.2" width="1.4" height="1.5"><feDropShadow dx="0" dy="9" stdDeviation="8" flood-color="#143b53" flood-opacity=".13"/></filter></defs>
<rect x="5" y="5" width="550" height="350" rx="28" fill="url(#bg)" stroke="#d8e5ed" stroke-width="2"/>
<circle cx="478" cy="92" r="37" fill="#dcecf1"/><circle cx="91" cy="259" r="25" fill="#dcecf1"/>
<g filter="url(#shadow)" stroke-linecap="round" stroke-linejoin="round">{drawing(symbol)}</g>
<rect x="157" y="286" width="246" height="31" rx="16" fill="#ffffff" stroke="#d8e5ed"/>
<text x="280" y="307" text-anchor="middle" font-family="system-ui,'Meiryo',sans-serif" font-size="16" font-weight="700" fill="#17445f">{label_xml}</text>
<text x="280" y="339" text-anchor="middle" font-family="system-ui,'Meiryo',sans-serif" font-size="11" letter-spacing=".09em" fill="#536879">製品カテゴリのイメージ</text>
</svg>
'''


def main() -> int:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    changed = 0
    articles = [p for p in sorted(SITE.glob("*.html")) if p.name != "index.html" and not p.name.startswith("google")]
    missing_symbols = [p.stem for p in articles if p.stem not in SYMBOLS]
    if missing_symbols:
        raise ValueError("Missing illustration categories: " + ", ".join(missing_symbols))
    for page in articles:
        source = page.read_text(encoding="utf-8")
        parsed = GuideParser()
        parsed.feed(source)
        if not parsed.affiliate_href:
            raise ValueError(f"Tagged Amazon search link not found in {page.name}")
        href = escape(parsed.affiliate_href, quote=True)
        category = category_name(parsed.title)
        label = escape(category, quote=True)
        query = escape(search_label(parsed.affiliate_href), quote=True)
        symbol = SYMBOLS[page.stem]
        image = f"assets/product-illustrations/{page.stem}.svg"
        (ASSET_DIR / f"{page.stem}.svg").write_text(render_svg(parsed.title, category, symbol), encoding="utf-8", newline="\n")
        figure = (
            '<p class="affiliate-note product-image-disclosure">画像・ボタンはAmazonアソシエイトリンクです。'
            '適格購入により紹介料を得る場合があります。</p>'
            f'<figure class="product-figure"><a class="product-image-link" href="{href}" '
            f'rel="sponsored nofollow noopener noreferrer" target="_blank"><img src="{image}" '
            f'alt="製品カテゴリのイメージ：{label}。クリックしてAmazon.co.jpで関連商品を探す" '
            'width="560" height="360" decoding="async"></a>'
            '<figcaption>特定商品の写真ではなく、製品カテゴリを示すオリジナルイラストです。'
            f'<br><a class="product-search-link" href="{href}" rel="sponsored nofollow noopener noreferrer" '
            f'target="_blank">Amazon.co.jpで「{query}」を探す ↗</a></figcaption></figure>'
        )
        if 'class="product-figure"' in source:
            source = re.sub(r'<p class="affiliate-note product-image-disclosure">.*?</figure>', figure, source, count=1, flags=re.DOTALL)
        else:
            insertion = re.search(r'(<div class="article-body"><p>.*?</p>)', source, re.DOTALL)
            if insertion is None:
                raise ValueError(f"Opening article paragraph not found in {page.name}")
            source = source[:insertion.end()] + figure + source[insertion.end():]
        page.write_text(source, encoding="utf-8", newline="\n")
        changed += 1
    print(f"Added product category illustrations and tagged search links to {changed} guides.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
