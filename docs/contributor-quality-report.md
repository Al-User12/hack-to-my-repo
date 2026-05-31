# Contributor Quality Report

Generated: 2026-05-31 12:03 UTC
Source: `Contributors.md`

## Snapshot

- Total entries scanned: **5010**
- Valid markdown links: **4463**
- Entries without links: **521**
- Hard errors: **31**
- Contributor Quality Score (CQS): **65.83/100 (D)**

## What this means

This repository intentionally welcomes first-time contributors. That creates a
high-volume, high-variance input stream in `Contributors.md`.

The quality toolchain keeps this beginner-friendly workflow scalable by:

1. detecting malformed links before merge,
2. documenting current debt transparently,
3. preventing regression in future pull requests.

## Top detected issues (sample)

- line 80: reversed scheme separator: 'https//:github.com/amidbashan'
- line 116: missing // after scheme: 'https:github.com/anjalisoni3655'
- line 204: empty link target
- line 263: looks like a URL but is not a markdown link -> '- [Domohina Malala]S (https://github.com/NyAina90)'
- line 290: looks like a URL but is not a markdown link -> '- [Jahshaka] (https://https://github.com/JahshakaDEV'
- line 379: missing scheme (add https://): 'github.com/jayfromhcomm'
- line 412: no URL scheme: 'https:/github.com/mikkrieg'
- line 413: no URL scheme: 'https:/github.com/'
- line 573: missing // after scheme: 'https:github.com/opyskoty'
- line 749: looks like a URL but is not a markdown link -> '- [Darshan][https://https://github.com/darshan-003]'
- line 854: no URL scheme: 'paper money pilgrim'
- line 894: missing scheme (add https://): 'www.github.com/prateek-ml'
- line 902: missing scheme (add https://): 'www.github.com/cat9563'
- line 1942: no URL scheme: 'CDavid-Damer'
- line 2311: missing // after scheme: 'https:github.com/rahulsinha2911'
- line 2313: missing // after scheme: 'https:github.com/nicvhub'
- line 2771: malformed scheme: 'https//github.com/feamoda'
- line 2772: malformed scheme: 'https//github.com/VinayMaurya001'
- line 3704: malformed github host: 'https://github.com./arpitansu'
- line 3785: missing scheme (add https://): 'github.com/PluckyPrecious'
- ... and 11 more

## Maintenance policy

- CI fails if hard errors exceed configured baseline.
- Baseline is intentionally lowered over time as old debt is cleaned.
- New PRs must not increase debt.
