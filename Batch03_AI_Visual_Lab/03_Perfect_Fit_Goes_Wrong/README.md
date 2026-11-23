# ArchitectByAI · AI Visual Lab · Batch 03, Video 03

## When Perfect Fit Goes Wrong

An original 18-second vertical Python animation demonstrating **overfitting**, using 11 noisy synthetic training observations drawn from a smooth ground-truth function. A degree-3 Chebyshev polynomial captures the broad pattern. A degree-10 Chebyshev polynomial interpolates all 11 points, but diverges on 101 different evaluation locations.

| Metric | Degree 3 | Degree 10 |
|---|---:|---:|
| Training RMSE | 0.0707 | ~0.0000 |
| Evaluation-position RMSE | 0.0222 | 0.9411 |

The evaluation-position comparison uses the known noiseless generating function on additional, predetermined x locations; it is a **synthetic demonstration**, not evidence of production model performance. Inputs are generated with NumPy random seed 96. A model with extremely low training error need not generalize well.

### Run

Requires Python, NumPy, Pillow and FFmpeg on your PATH.

```bash
python -m pip install -r requirements.txt
python animation.py --output B03_V03_Overfitting_1080x1920.mp4
```

The video renders 360 unique animation frames at 20 FPS, drawn natively at 540×960 and Lanczos-upscaled to 1080×1920 for delivery. Uses only original generated graphics and no licensed music, stock footage or third-party image assets. Output includes cover and evidence frames locally. The published GitHub repository contains **source and documentation only, no MP4**.

**Single featured offer:** AI Assistants & Chatbots service at architectbyai.com. Founder controls actual social publication.