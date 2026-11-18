# ArchitectByAI · Batch 02 — New Productions (Episodes 04–07)

This is a **new four-episode release**, not a re-export of the seven-video Nov 12 preview ZIP.

| Ep | Product | Original visual mechanism | Color identity |
| --- | --- | --- | --- |
| 04 | Create & Sell Digital Products | 3D laptop workspace continuously assembles creative tiles; finished digital products emerge into a cinematic studio | Midnight indigo, violet, champagne gold |
| 05 | Marketing & Customer Communication Kit | One inquiry routes into a communication system; animated message connections resolve into a real interface and return a reply | Deep teal, copper, cyan |
| 06 | Client Onboarding & Proposal Toolkit | Inquiry traces a path into a growing proposal, signature and delivery milestones | Plum, rose, gold |
| 07 | Magical Friends Coloring Toolkit | Mathematical curves draw an original butterfly silhouette; the character reveals detailed fine-line and colored art | Midnight blue, lilac, turquoise, pink |

Each video contains a hook, evolving story text, an animated mechanism, the product name, `FOLLOW @architectbyai`, and `architectbyai.com` in a contained closing panel. Every caption states **Using Python**.

**Publishing:** Episode 01 was previously posted; do not repost it. Episodes 02 and 03 have separate historical files. This folder contains only genuinely new 04–07 outputs. Confirm post status before scheduling.

## Render (Linux)

Requirements: Python 3, Pillow, NumPy, FFmpeg, and (for episode 04 only) Blender 4.3+.

```bash
pip install -r requirements.txt
python render_release.py --episode 05
python render_release.py --episode 06
python render_release.py --episode 07
```

Episode 04 is the only one with animated Blender 3D source:

```bash
blender --background --factory-startup --python 04_Digital_Product_Studio/blender_scene.py
ffmpeg -framerate 12 -i 04_Digital_Product_Studio/frames/frame_%04d.png -vf "minterpolate=fps=20:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1" -an -c:v libx264 -crf 18 -pix_fmt yuv420p 04_Digital_Product_Studio/3d_raw.mp4
python render_release.py --episode 04
```

The source renderer outputs 540×960, 20 fps, 16-second H.264/yuv420p MP4s; no music/audio. `*_POST_1080x1920.mp4` files are **Lanczos-upscaled posting exports** (1080×1920 delivery canvas, not a native 1080-line 3D render). The 3D frame sequence is generated locally (not committed).

The `cinematic_plate.png` files are original image-generated backgrounds, integrated into original Python/Blender motion graphics. Small `cinematic_plate.jpg` equivalents are valid for GitHub source release. No third-party footage. The motion code is original and does not use the Manim runtime directly—do not label the result as Manim-rendered. It belongs to the ArchitectByAI math-and-art content series and is Python procedural animation.

## GitHub / packaging

Repository: https://github.com/ArchitectByAI/manim-math-art

Suggested destination: `Batch02_Digital_Products/`. Include source, instructions, plates, and text only. **Do not commit MP4s, rendered Blender PNG frame sequences, or generated draft/review images.**

Posting material is in one file: `ALL_CAPTIONS_AND_PINNED_COMMENTS.txt`. No duplicated per-platform caption files.

## Quality checks before posting

- Watch the entire video on a phone to check hook and visual motion, not just 5 contact-sheet stills.
- Confirm on-screen text is legible and does not overlap visual objects or frame edges.
- Check the product exists and the website destination actually works before publishing.
- Log each post's views, saves, follows, website visits, inquiries and purchases.
- No invented claims of sales, performance, or successful automations are made.
