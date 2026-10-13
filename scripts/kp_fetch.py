#!/usr/bin/env python3
"""Fetch the Socialist Constitution of the DPRK as published on Naenara (naenara.com.kp, the
official web portal of the DPRK, operated by the Foreign Languages Publishing House), from
Internet Archive (Wayback Machine) captures, in Korean (ko) and the official English translation (en).

naenara.com.kp is not reachable from here (connection time-out). The most recent complete
captures of the constitution pages (/<lang>/great/constitution.php?1..15) are used.
Usage: kp_fetch.py RAW_DIR
"""
import json, os, sys, time
import requests

UA = "LawCodex/1.0 (+https://github.com/LawCodex)"
RAW = sys.argv[1]
S = requests.Session()
S.headers["User-Agent"] = UA


def req(url):
    for a in range(6):
        try:
            r = S.get(url, timeout=180)
            if r.status_code == 200:
                return r
            print("HTTP", r.status_code, url, file=sys.stderr)
        except Exception as e:
            print("ERR", url, e, file=sys.stderr)
        time.sleep(10 * 2 ** a)
    raise RuntimeError(url)


def main():
    out = os.path.join(RAW, "naenara")
    os.makedirs(out, exist_ok=True)
    index = []
    for lang in ("ko", "en"):
        cdx = req("http://web.archive.org/cdx/search/cdx?url=naenara.com.kp/%s/great/constitution.php"
                  "&matchType=prefix&filter=statuscode:200&fl=original,timestamp,length" % lang).text
        for n in range(1, 16):
            caps = [l.split() for l in cdx.splitlines()
                    if l.split()[0].endswith(f"constitution.php?{n}") and int(l.split()[2]) > 2000]
            if not caps:
                print("no capture", lang, n)
                continue
            url, ts, _ = max(caps, key=lambda c: c[1])
            p = os.path.join(out, f"{lang}_{n:02d}.html")
            if not os.path.exists(p):
                r = req(f"https://web.archive.org/web/{ts}id_/{url}")
                open(p, "wb").write(r.content)
                time.sleep(2)
            index.append({"lang": lang, "page": n, "url": url, "timestamp": ts,
                          "archived_url": f"https://web.archive.org/web/{ts}/{url}", "file": p})
    json.dump(index, open(os.path.join(RAW, "index.json"), "w"), indent=1)
    print(len(index), "pages")


if __name__ == "__main__":
    main()
