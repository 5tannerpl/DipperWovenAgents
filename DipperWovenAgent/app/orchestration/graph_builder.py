from langgraph.graph import END, START, StateGraph

from app.orchestration.state import DipperWovenAgentState
from app.understanding.event_detector import event_detection_node
from app.understanding.input_normalizer import input_normalization_node
from app.understanding.question_decomposer import (
    question_decomposition_node,
)


def build_graph():

    builder = StateGraph(
        DipperWovenAgentState
    )

    builder.add_node(
        "input_normalization",
        input_normalization_node,
    )

    builder.add_node(
        "event_detection",
        event_detection_node,
    )

    builder.add_node(
        "question_decomposition",
        question_decomposition_node,
    )

    builder.add_edge(
        START,
        "input_normalization",
    )

    builder.add_edge(
        "input_normalization",
        "event_detection",
    )

    builder.add_edge(
        "event_detection",
        "question_decomposition",
    )

    builder.add_edge(
        "question_decomposition",
        END,
    )

    return builder.compile()