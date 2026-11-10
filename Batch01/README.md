# ArchitectByAI — Python Animation Batch 01

Seven vertical procedural animations created **using Python**. Despite the historical “Manim 2.0” batch name, these are **Pillow/NumPy procedural animations, not Manim scenes**.

## Episodes
1. [Magical Garden](01_Magical_Garden/) — botanical geometry
2. [Neural Network Learns](02_Neural_Network_Learns/) — illustrative neural network
3. [Chaos Creates Beauty](03_Chaos_Creates_Beauty/) — simulated double pendulum
4. [Data to Intelligence](04_Data_to_Intelligence/) — data cleaning and KPIs
5. [Automation Engine](05_Automation_Engine/) — business workflow
6. [Drawing with Fourier](06_Drawing_with_Fourier/) — epicycles
7. [Digital Experience](07_Digital_Experience/) — website wireframe to interface

## Reproduce

Install Python 3, FFmpeg, and the Python packages:

```bash
pip install -r requirements.txt
```

Episode 01 is self-contained: `python 01_Magical_Garden/animation.py`. It writes an 8-second 540×960 preview and a PNG.

Episodes 02–07 share the full `render_batch.py` source:

```bash
python render_batch.py --episode 2
python render_batch.py --all
```

Or run each episode's `animation.py` entrypoint. These write 12-second 1080×1920 videos under `Episode_02_Neural_Network_Learns/`, etc. FFmpeg must be available on PATH. Fonts are configured for Linux DejaVu Sans paths; adjust the `FONT` and `BOLD` paths on Windows/macOS.

**GitHub contains source code and documentation only; no MP4 files.**
