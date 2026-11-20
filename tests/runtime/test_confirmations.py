from google.adk.events import Event
from google.genai import types

from aurora.runtime.conversation import ConversationService


def test_confirmation_parser_exposes_only_safe_details() -> None:
    call = types.FunctionCall(
        id="confirmation-1",
        name="adk_request_confirmation",
        args={
            "originalFunctionCall": {
                "id": "tool-call-1",
                "name": "reserve_common_area",
                "args": {
                    "area": "salao-de-festas",
                    "data": "2030-04-20",
                    "apartamento": "302",
                },
            }
        },
    )
    event = Event(
        invocation_id="invocation-1",
        author="especialista_reservas",
        content=types.Content(
            role="model",
            parts=[types.Part(function_call=call)],
        ),
        long_running_tool_ids={"confirmation-1"},
    )

    active = ConversationService._active_confirmations([event])

    assert active["confirmation-1"].details == {
        "area": "salao-de-festas",
        "data": "2030-04-20",
    }
    assert "302" not in str(active["confirmation-1"].details)


def test_answered_confirmation_is_not_active() -> None:
    request = Event(
        invocation_id="invocation-1",
        author="especialista_visitantes",
        content=types.Content(
            role="model",
            parts=[
                types.Part(
                    function_call=types.FunctionCall(
                        id="confirmation-1",
                        name="adk_request_confirmation",
                        args={"originalFunctionCall": {"name": "authorize_visitor"}},
                    )
                )
            ],
        ),
        long_running_tool_ids={"confirmation-1"},
    )
    answer = Event(
        invocation_id="invocation-1",
        author="user",
        content=types.Content(
            role="user",
            parts=[
                types.Part(
                    function_response=types.FunctionResponse(
                        id="confirmation-1",
                        name="adk_request_confirmation",
                        response={"confirmed": True},
                    )
                )
            ],
        ),
    )

    assert ConversationService._active_confirmations([request, answer]) == {}
