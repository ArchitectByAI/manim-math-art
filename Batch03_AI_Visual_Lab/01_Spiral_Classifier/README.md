# ArchitectByAI — Batch 03 / Pilot 01

**Working title:** Can AI Untangle Two Spirals?

**Status:** RENDERED and technical QA checked. **Awaiting founder creative approval.** Not published on social media, not uploaded to GitHub. This is a separate production ID, not a new sequential public episode number.

## What the experiment actually does

`animation.py` generates 210 synthetic observations from two noisy intertwined spirals. It maps 2D observations into 280 random Fourier features, then trains logistic classification weights with full-batch gradient descent and L2 regularization. The displayed background colors are computed from the model's learned decision function for the shown training checkpoint. The percentage is *training-set classification accuracy*, not out-of-sample performance or an AI product accuracy guarantee.

**Technical result:** training accuracy goes from 50% to 99.52% after 440 gradient updates. Decision regions can contain extra artifacts away from sampled observations; this is a property of the illustrative model, not an attempt to conceal uncertainty.

## Reproduce

Python 3.10+; `pip install -r requirements.txt`; FFmpeg on PATH.

```bash
python animation.py
```

The renderer generates an 18-second 540×960 20fps MP4. The posting export is Lanczos-upscaled to 1080×1920; it is **not native 1080p source footage**:

```bash
ffmpeg -i Batch03_01_SpiralAI.mp4 -vf scale=1080:1920:flags=lanczos -c:v libx264 -crf 19 -pix_fmt yuv420p Batch03_01_SpiralAI_POST_1080x1920.mp4
```

No music, narration or third-party footage. Sound is intentionally absent; the animation is comprehensible when muted. Use no claims of live tool integration or measured test-set generalization.

## Editorial sequence

- 0–2.5s: immediately visible question, two intertwined point spirals assemble
- 2.5–6s: learning starts; classifier field evolves from one color to a nonlinear boundary
- 6–14s: progressively trained decision regions change using authentic training checkpoints
- 14–16s: static screenshot-friendly model insight card
- 16–18s: exactly one featured offer, **Data Intelligence** service, with **architectbyai.com**; no prices

## QA & governance

- MP4 posting export: 1080×1920, 20fps, 360 frames, 18.00s; FFmpeg full-decode pass.
- Screens sampled from opening, mid-training, reveal, save card, final service end card.
- End-card website visible; no public source link claim before GitHub push.
- **Founder approval required** before GitHub source release or any external publication.
- Historical Episode 07 is the wireframe. This pilot has no episode number. Rejected coloring content remains excluded.


## Correction / distribution
Brand masthead corrected from “VISUAL PROOF 03” to “AI VISUAL LAB”. Native renderer is 540×960 at 20 fps; posting MP4 is Lanczos-upscaled 1080×1920 (not native 1080). The MP4, still frames, and private QA material are not stored in this public source repository. No live course enrollment claim.