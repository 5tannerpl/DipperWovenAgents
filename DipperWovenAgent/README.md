# DipperWovenAgent

import time

start = time.perf_counter()

response = await llm_client.chat.completions.create(
    ...
)

elapsed = time.perf_counter() - start

usage = response.usage

cached = 0
if usage.prompt_tokens_details:
    cached = usage.prompt_tokens_details.cached_tokens or 0

print(
    f"[LLM] "
    f"time={elapsed:.2f}s | "
    f"input={usage.prompt_tokens} | "
    f"cached={cached} | "
    f"output={usage.completion_tokens} | "
    f"total={usage.total_tokens}"
)
