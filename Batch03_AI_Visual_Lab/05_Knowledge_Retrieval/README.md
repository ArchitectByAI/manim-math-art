# ArchitectByAI — Batch 03 / Video 05

**How Does AI Find the Right Answer?** A scientifically grounded visual explanation of lexical document retrieval used as one component in AI knowledge systems.

## What is real

The Python animation code constructs an original, fictional business knowledge base containing five documents and the question "How long do refunds take?". It computes log-scaled term frequency times smoothed inverse-document-frequency and normalized cosine similarities; **returns policy ranks first at cosine ~0.2711**. The figures and displayed content are calculated from the same source code, not invented numbers. This is **not** a neural embedding model, full LLM, production RAG retrieval service, or evaluated answer accuracy benchmark.

**Promotional context:** One featured service, ArchitectByAI Lead Qualification & Knowledge Systems, with website architectbyai.com. No prices. No claim of live course enrollment.

## Reproduce the video

Requirements: Python 3.10+, NumPy, Pillow, FFmpeg on PATH.

```bash
python -m pip install -r requirements.txt
python animation.py
```

Output is a silent H.264 1080x1920 video upscaled from a native 540x960 procedural animation at 20fps for 18 seconds. Source produces private review stills (`opening.png`, `ranking.png`, `answer.png`, `end.png`, `cover.png`) on local render. **Do not upload the MP4 or frames into the GitHub repository.** The founder publishes manually.

## Verified science

The five-document vectorizer excludes query text when calculating document frequency. Each candidate is scored using cosine similarity to the question vector. The ranking is computed at runtime, with a tested assertion that the fictional Returns Policy is the top match. The highlighted document text is authored for this synthetic illustration and not a real business's refund policy.

## Production

- Rendered November 25, 2026
- Working content ID: B03-V05-KNOWLEDGE
- 18 seconds / 360 frames / 20 FPS / 9:16
- Brand header: `ARCHITECTBYAI | AI VISUAL LAB` (no confusing numbered Visual Proof tag)
- Captions and pinned comments: `POSTING_PACKAGE.md`
- Social publishing: founder approval and manual publication only