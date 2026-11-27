# ArchitectByAI AI Visual Lab — Batch 03 Video 07

## Can Code Find the Best Route?

An original 18-second vertical animation of a **real Dijkstra shortest-path calculation** on a synthetic ten-node, seventeen-edge undirected graph. Start A, target J. The deterministic shortest path is `A → D → H → I → J` with total weight `16`.

**Accuracy / scope:** All nodes and edge costs are invented for illustration. They are not road distances, travel times, business metrics, customer data, or an actual business automation pipeline. The association with ArchitectByAI's Business Process Automation service is a thematic example of algorithmic decision-making—not proof of a commercial software product already deployed. The algorithm is implemented in `animation.py` using `heapq`, and the asserted result recomputes the shortest-path weight.

## Reproduction

Install Pillow 9+ and FFmpeg. Run:

```bash
python animation.py
```

The script renders 360 frames at a native 540x960 and upscales with FFmpeg Lanczos to 1080x1920 20fps H.264. Sound is intentionally absent. The source is original and deterministic; the system font path uses DejaVu Sans on Linux and may require adaptation on Windows.

## Video beats

0–3s: hook and network reveal with early follow cue. 3–11.7s: weighted graph explored in Dijkstra visit order. 11.7–14s: shortest route revealed. 14–16s: screenshot-worthy Dijkstra insight. 16–18s: exactly one featured offer, Business Process Automation, architectbyai.com.

No prices, enrollment claims or external footage. The MP4 is delivered separately and deliberately excluded from GitHub.