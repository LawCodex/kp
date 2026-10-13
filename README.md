# LawCodex — Democratic People's Republic of Korea (`kp`)

The **Socialist Constitution of the Democratic People's Republic of Korea** (조선민주주의인민공화국
사회주의헌법) as plain Markdown, in Korean (the original) and in the English translation published by
the DPRK state portal *Naenara*.

Part of [LawCodex](https://github.com/LawCodex): the legislation of every country as Markdown in git.

Retrieved: **2026-10-13**.

## Contents

| File | Language | Version | Articles |
|---|---|---|---:|
| `constitution/socialist-constitution-ko.md` | Korean (original) | as amended 29 June 2016 | 172 |
| `constitution/socialist-constitution-en.md` | English (Naenara translation) | as amended 29 June 2016 | 172 |

The constitution was adopted on 27 December 1972 and has been amended several times. The text here
is the version that introduced the State Affairs Commission (amendment of 29 June 2016), which is the
most recent complete text that could be obtained from an official DPRK publication.

## What is NOT covered

- **Later amendments** (April 2019, August 2019, September 2023 and any later ones) — no complete
  official text of these versions could be obtained (see below).
- Other DPRK laws: the DPRK does not publish a public online legislation database. No other
  statutes are included.

## Sources

- Publisher: *Naenara* (내나라, `naenara.com.kp`), the official web portal of the DPRK, operated by
  the Foreign Languages Publishing House. Pages: `http://www.naenara.com.kp/ko/great/constitution.php?1`…`?15`
  (Korean) and `http://www.naenara.com.kp/en/great/constitution.php?1`…`?15` (English).
- `naenara.com.kp` could not be reached directly at retrieval time (connection time-out), so the
  pages were taken from **Internet Archive (Wayback Machine) captures of 23 September 2016**, e.g.
  <https://web.archive.org/web/20160923202722/http://www.naenara.com.kp/ko/great/constitution.php?1>.
  The archived URL of each of the 15 pages is listed in the front matter (`archived_sources`).

- The current Naenara site (`/main/index/<lang>/politics?arg_val=constitution`) loads the text
  chapter by chapter via script; only the preamble of that version was archived, so it could not
  be used.
- Copyright notice on Naenara: "© Foreign Languages Publishing House of the DPRK". The constitution is
  an official legal text, reproduced verbatim (text only). This repository is not an official
  publication.

## Format

Headings: `## 제N장` / `## CHAPTER …`, `### 제N절` / `### SECTION …`, `#### 제N조` / `#### Article N.`.
Article text paragraphs follow each heading.

## Regenerate

```sh
python3 scripts/kp_fetch.py   ../_raw/kp     # Wayback CDX lookup + latest complete capture of each page
python3 scripts/kp_convert.py ../_raw/kp .
```
