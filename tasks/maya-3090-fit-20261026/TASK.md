# maya-3090-fit-20261026

Goal: find out whether Project Maya can run a large MoE model usefully on ONE RTX 3090 with 62 GB RAM plus NVMe, so we know if a 1-hour test is worth it.

Public research only. Repo: https://github.com/mw00/project-maya (MIT). Claim seen on X (@JoeGuglielmucci, 2026-10-25): "KV history in RAM, recent window in VRAM -> 1M context fits a single 3090".

RESULT must contain (under 1 page, sources linked):
1. Which model/quant fits 1x 24 GB GPU + 62 GB system RAM with the rest streamed from NVMe (README says Maya-S24 is 94.7 GB)? Any user reports (GitHub issues/discussions) of single-3090 runs: tokens/s decode and prefill, context length used.
2. Is the "1M context on one 3090" claim real for that setup, or only with more RAM/GPUs? Quote the source.
3. How much NVMe read traffic per token does expert streaming cause (SSD wear is a concern: reads are fine, writes are not; does it write?).
4. Build/run requirements: Docker/Podman image available? CUDA version? Anything that must run as root?
5. Verdict: worth a 1-hour test on a single 3090 or not, in one line.

Rules: public pages only, no login, no account, no purchase, no messages or comments to anyone. A link and read date for every fact. Say "unsure" rather than guess. End with **How I checked it** and **Unsure about**.

Delivery: reply in this chat with the full RESULT block: first line `RESULT maya-3090-fit-20261026`, then the complete answer in Markdown (write every source as a full https:// link in plain text), last line `END maya-3090-fit-20261026`. Also push `results/maya-3090-fit-20261026/RESULT.md` to GitHub only if asked.
