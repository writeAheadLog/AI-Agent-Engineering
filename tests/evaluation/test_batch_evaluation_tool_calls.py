import importlib
import json

import pytest
from langchain_core.messages import AIMessage, ToolMessage

SCENARIO = json.dumps({
    "sample_id": "cancel_1",
    "input": [{"role": "user", "content": "Please cancel order B73973."}],
    "expected_function_call": {"name": "cancel_order", "arguments": {"order_id": "B73973"}},
})


class FakeGraph:
    """Returns messages shaped like langchain-openai 1.x output: tool calls live on AIMessage.tool_calls only."""

    def invoke(self, state):
        return {"messages": [
            *state["messages"],
            AIMessage(content="", tool_calls=[{"name": "cancel_order", "args": {"order_id": "B73973"}, "id": "call_1"}]),
            ToolMessage(content="cancelled", tool_call_id="call_1"),
            AIMessage(content="Your order B73973 has been cancelled."),
        ]}


@pytest.mark.parametrize("module", ["ch09.batch_evaluation", "ch09.evaluation.batch_evaluation"])
def test_tool_calls_on_ai_message_are_scored(module):
    evaluate = importlib.import_module(module).evaluate_single_instance

    result = evaluate(SCENARIO, FakeGraph())

    assert result["tool_recall"] == 1.0
    assert result["tool_precision"] == 1.0
    assert result["param_accuracy"] == 1.0
