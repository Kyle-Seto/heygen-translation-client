from typing import TypedDict, Literal

class StatusResponse(TypedDict):
    """Type definition for status response."""
    result: Literal["pending", "completed", "error"]
