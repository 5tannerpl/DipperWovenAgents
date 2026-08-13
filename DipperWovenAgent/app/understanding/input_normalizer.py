"""Input normalization utilities."""

import re

from app.orchestration.state import DipperWovenAgentState


async def input_normalization_node(
    state: DipperWovenAgentState,
) -> dict:

    raw_input = state["raw_input"]

    normalized = re.sub(
        r"\s+",
        " ",
        raw_input.strip(),
    )

    return {
        "normalized_input": normalized
    }