# Batch 03 — Video 06: Can Data Reveal Hidden Groups?

A deterministic 18-second, 9:16 visual experiment using **actual K-means** with NumPy and Pillow procedural graphics. The 102 points are synthetic and arranged in three clear clusters. K is explicitly preset to 3; the algorithm does not choose K. Iteration uses nearest-centroid assignments and updates each centroid to the mean of its assigned points until convergence. The script prints group sizes; labels are relative to the chosen random initial centers and have no intrinsic meaning.

## Render

Requirements: Python 3.10+, `numpy`, `Pillow`, `ffmpeg` executable on `PATH`.

```bash
pip install -r requirements.txt
python animation.py --output video.mp4
```

Rendered at 540×960, upscaled with FFmpeg Lanczos to 1080×1920 H.264 at 20 FPS, 360 frames, 18 seconds; no licensed music or external visual assets. Script exports cover and QA stills locally. Posting MP4s are not kept in this GitHub repository. The script uses DejaVu fonts installed at `/usr/share/fonts/truetype/dejavu/`; adjust paths if running on a system without them.

## Accuracy and limits
- The synthetic points come from `numpy.random.default_rng(20261126)` with three center locations.
- The initial centroids are deliberately imperfect; algorithm converges in four reassignment/mean-update iterations on this data.
- The visual demonstration illustrates grouping, **not** validated customer segmentation or product functionality.
- Featured offer: ArchitectByAI **Marketing & Customer Communication Kit**. The kit is marketed separately and is not represented as a clustering tool.

## Publishing

See `POSTING_PACKAGE.md`. Founder manually reviews and posts. All social captions preserve the single-offer rule and direct traffic to architectbyai.com.