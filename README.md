# manim-math-art
# 🌌 manim-math-art
**By [ArchitectByAI](https://linktr.ee/architectbyai)**

A collection of programmatic, loopable math and physics animations created using Python and the Manim engine. Designed for high-retention short-form content (TikTok, Reels, Shorts).

## 🎬 Current Animations
* **Cardioid Envelope:** Generating a cardioid by drawing 120 circles through a fixed point on a base circle. 
  * File: `cardioid.py`
  * Concept: Epicycloid Geometry

## ⚙️ How to Run Locally

**1. Clone the repository**
```bash
git clone D:\ArchitectByAI_Projects\manim-math-art\manim-math-art\cardioid.py
cd manim-math-art

2. Install dependencies Make sure you have Python installed, as well as FFmpeg and LaTeX (for rendering text/math).
bash


pip install -r requirements.txt
3. Render the video To generate the 9:16 vertical video for social media:
bash


manim -pql cardioid.py Epicycloid
(Note: -pql renders in low quality for quick testing. Use -pqh for high quality 1080p final rendering).
