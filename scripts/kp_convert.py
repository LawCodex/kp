#!/usr/bin/env python3
"""Convert the archived Naenara constitution pages (see kp_fetch.py) into Markdown.

Usage: kp_convert.py RAW_DIR OUT_DIR
"""
import datetime, json, os, re, sys
from bs4 import BeautifulSoup

RAW, OUT = sys.argv[1], sys.argv[2]
TODAY = datetime.date.today().isoformat()

META = {
    "ko": {"title": "조선민주주의인민공화국 사회주의헌법",
           "file": "socialist-constitution-ko.md"},
    "en": {"title": "Socialist Constitution of the Democratic People's Republic of Korea",
           "file": "socialist-constitution-en.md"},
}


def clean(t):
    t = t.replace("﻿", "").replace("\xa0", " ")
    return re.sub(r"[ \t]+", " ", t).strip()


def page_md(path):
    soup = BeautifulSoup(open(path, "rb").read().decode("utf-8", "replace"), "lxml")
    nav = soup.find(string=re.compile(r"\d+\s*/\s*15"))
    td = nav.find_parent("tr").find_next_sibling("tr").find("td")
    out = []
    for tr in td.find_all("tr"):
        tds = tr.find_all("td", recursive=False)
        if not tds:
            continue
        if len(tds) == 1:
            if len(tds[0].get_text()) > 150:
                for br in tds[0].find_all("br"):
                    br.replace_with("\n")
                out += [clean(x) for x in tds[0].get_text("").split("\n") if clean(x)]
                continue
            txt = clean(tds[0].get_text(" "))
            if txt:
                lvl = "##" if re.match(r"^(제\s*\d+\s*장|CHAPTER|PREAMBLE|서\s*문)", txt, re.I) else "###"
                out.append(f"{lvl} {txt}")
            continue
        label = clean(tds[0].get_text(" "))
        for br in tds[1].find_all("br"):
            br.replace_with("\n")
        paras = [clean(p) for p in tds[1].get_text("").split("\n")]
        paras = [p for p in paras if p]
        if label:
            out.append("#### " + label.rstrip(":").strip())
        out += paras
    # pages without a table (e.g. the preamble) — take the paragraphs
    if not out:
        for p in td.find_all(["p", "b"]):
            txt = clean(p.get_text(" "))
            if txt:
                out.append(txt)
    return out


def main():
    idx = json.load(open(os.path.join(RAW, "index.json")))
    for lang, meta in META.items():
        pages = sorted([x for x in idx if x["lang"] == lang], key=lambda x: x["page"])
        body = []
        for x in pages:
            body += page_md(x["file"])
        # first heading of the preamble page
        if body and not body[0].startswith("#"):
            body.insert(0, "## " + ("서문" if lang == "ko" else "PREAMBLE"))
        body = [("## " + b) if b in ("PREAMBLE", "서 문", "서문") else b for b in body]
        fm = ["---", f'title: "{meta["title"]}"', 'identifier: "DPRK Socialist Constitution (as amended 29 June 2016)"',
              "type: constitution", "jurisdiction: kp", f"language: {lang}",
              "date: 1972-12-27", "last_amended: 2016-06-29", "status: unknown",
              f'source: "http://www.naenara.com.kp/{lang}/great/constitution.php"',
              f'archived_source: "{pages[0]["archived_url"]}"',
              f'archived_pages: "{len(pages)} pages, Wayback Machine captures of {pages[0]["timestamp"][:8]}"',
              "publisher: \"Naenara (Foreign Languages Publishing House, DPRK)\""]
        if lang == "en":
            fm.append('note: "English translation as published by Naenara; the Korean text is the original"')
        fm += [f"retrieved: {TODAY}", "---", ""]
        p = os.path.join(OUT, "constitution", meta["file"])
        os.makedirs(os.path.dirname(p), exist_ok=True)
        # drop duplicated preamble heading
        txt = "\n\n".join(body)
        txt = re.sub(r"^## (PREAMBLE|서문)\n\n## (PREAMBLE|서 ?문)\n", r"## \2\n", txt)
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(fm) + f"# {meta['title']}\n\n" + txt + "\n")
        print(p, len(txt))


if __name__ == "__main__":
    main()
