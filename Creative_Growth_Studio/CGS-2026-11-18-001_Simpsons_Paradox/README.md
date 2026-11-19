# Creative Growth Studio — Simpson's Paradox Pilot

**Pilot ID:** `CGS-2026-11-18-001`  
**State:** founder-approved for source release; video publication remains separately controlled.  
**Release:** source code and supporting documentation released in this GitHub folder; the MP4 is not stored in GitHub and has not been authorized for social publishing.  
**Lead concept:** Can the Same Data Point Both Ways?  
**One offer:** Upcoming Visual Data Science Lessons — coming soon.

## Contents

- Finished 18.0-second private video: native 1080×1920, 24fps, H.264/yuv420p plus AAC original synthetic sound; **not stored in GitHub**.
- Thumbnail is in the private production handoff, not this public repository.
- `simpsons_paradox.py`: complete original Python animation source, deterministic synthetic data and optional generated audio.
- `POSTING_PACKAGE.md`: Instagram, TikTok, YouTube Shorts copy and pinned comments.
- `STORYBOARD.md`: time-coded mechanism proof and editorial choices.
- Motion/QA evidence remains in private production handoff and is not committed.
- `performance_tracker.csv`: publication and conversion tracking template.
- `requirements.txt`: Python dependencies.

## Run the source

Requirements: Python 3.10+, NumPy, Pillow and FFmpeg installed and on PATH. On Linux, install these Python dependencies with `pip install -r requirements.txt`. On Windows, install FFmpeg separately and set PATH. System fonts: InterDisplay if installed or Windows Arial/Arial Black; a local copy of fonts is not bundled or licensed for distribution.

```bash
python simpsons_paradox.py --out rebuilt.mp4
python simpsons_paradox.py --out small_proof.mp4 --width 540 --fps 12
python simpsons_paradox.py --still 0.75 --out still.png
```

## Statistical reproducibility

All 56 synthetic (not real-world) data points come from a fixed seeded RNG. Fits computed by `numpy.polyfit`:

- Group A slope `+0.643447`
- Group B slope `+0.636220`
- Pooled slope `-0.786408`

Positive subgroup fits and negative pooled fit are asserted before rendering. This is a valid demonstration of Simpson's paradox, not a causal inference or proof of generality. Slope and fit lines are computed from exactly the same data that is drawn; nothing is hand-faked.

## Permissions, release and ledger

The completed MP4 remains a **private founder-review artifact**. This folder contains only approved educational source and documentation. Do not upload the MP4, rendered frame previews, customer data, or private artwork. Do not publish the video to social media without separate founder authorization. Give it a permanent public episode number only after checking the actual published ledger. The historical wireframe is already Episode 07; the coloring-book concept is canceled.