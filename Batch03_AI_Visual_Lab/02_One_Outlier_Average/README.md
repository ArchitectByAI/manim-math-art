# ArchitectByAI · AI Visual Lab · Batch 03 Video 02

## Can One Number Hijack the Average?

An original, scientifically correct Python/Pillow/NumPy 18-second vertical animation demonstrating the sensitivity of a mean to an extreme outlier versus the robustness of the median. The dataset is **synthetic** and not representative of real customers or measured business performance.

Original values: `10, 11, 12, 12, 13, 14, 15, 16, 17`.

| Dataset | n | Mean | Median |
| --- | ---: | ---: | ---: |
| Original | 9 | 13.333... | 13.0 |
| Original + 150 | 10 | 27.0 | 13.5 |

The vertical chart scale changes visibly from 0–22 to 0–160 to accommodate the outlier. Do not interpret the interpolated vertical display transition as real time-series data. The numbers in the statistic cards are computed from the exact arrays in `animation.py`.

### Production

- Python 3.10+, NumPy, Pillow, FFmpeg on PATH.
- `pip install -r requirements.txt`
- `python animation.py --output native_540x960.mp4`
- Posting export with `ffmpeg -i native_540x960.mp4 -vf scale=1080:1920:flags=lanczos -c:v libx264 -crf 19 -pix_fmt yuv420p final_1080x1920.mp4`
- 18 seconds, 18 fps, 324 video frames; 540×960 native and 1080×1920 upscaled delivery, **not** native 1080p. No audio track; works silent.
- Private MP4, thumbnail, images, and QA files are **not** published in the GitHub source folder.
- Exactly one featured offer: KPI Dashboard Toolkit, directing viewers to architectbyai.com. No prices are included.

### Release & rights

Original deterministic Python visuals and synthetic demonstration. No third-party footage or audio. The provided GitHub source is educational; the paid KPI Dashboard Toolkit itself is not included.

### Posting

`POSTING_PACKAGE.md` contains Instagram, TikTok, and YouTube Shorts captions and pinned comments. Founder publishes manually. An approved source release does not mean the video was published to social accounts.