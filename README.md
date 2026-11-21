# The World in One Picture — 21 November 2026

One image summing up the world news of Saturday 21 November 2026.

## How it works

`main.py` (Python 3, Pillow) draws a newspaper-style front page and writes
it to `/output/entry.png`. It is fully deterministic: no network, no clock,
no randomness — two runs write byte-identical files. If Pillow is ever
unavailable, it copies the bundled `entry.png` (the same picture) instead.

## The day's stories (all first reported on 21 November 2026)

- **Peru — 6.8 quake shakes central Peru.** The tremor struck the Andean
  region of Junín (01:09 UTC), was felt in Lima, and sent residents rushing
  outdoors. No casualties reported. (Reuters, USGS, Peru's Geophysical
  Institute)
- **China — Trump, Xi and Putin meet.** Leaders hold a historic trilateral
  summit in China.
- **Ukraine — Russia hits Kyiv bridges.** Missiles strike three bridges;
  2 dead, 42 hurt in Kryvyi Rih.
- **Europe — Poland seeks NATO help.** After Russian aircraft breach its
  airspace.
- **India — record cash into Indian shares.** ₹1.22 lakh crore in November,
  the biggest monthly foreign inflow on record (depository data).
- **Sport — Rahul completes the SENA set.** First Indian opener with Test
  centuries in South Africa, England, New Zealand and Australia — 100 in
  Wellington.

## Image

- 1024 × 1024 PNG, 111,215 bytes (limit: 1 MiB, 1024 × 1024)
- The date "SATURDAY 21 NOVEMBER 2026" is prominent at the top; every story
  is readable from the image alone.

## Run it

```sh
python3 main.py            # writes /output/entry.png
python3 main.py out.png    # or any path, for testing
```
