from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class UserState:
    """State for a single user in the upsell flow."""

    messages: int = 0
    voice_offered: bool = False
    voice_sent: bool = False
    video_offered: bool = False


class UpsellManager:
    """Tracks interaction state and decides when to propose paid content."""

    def __init__(self, free_message_limit: int = 3):
        self.free_message_limit = free_message_limit
        self._states: dict[int, UserState] = defaultdict(UserState)

    def record_message(self, user_id: int) -> None:
        self._states[user_id].messages += 1

    def needs_voice_offer(self, user_id: int) -> bool:
        state = self._states[user_id]
        return state.messages >= self.free_message_limit and not state.voice_offered

    def record_voice_offered(self, user_id: int) -> None:
        self._states[user_id].voice_offered = True

    def record_voice_sent(self, user_id: int) -> None:
        state = self._states[user_id]
        state.voice_sent = True
        state.voice_offered = True

    def needs_video_offer(self, user_id: int) -> bool:
        state = self._states[user_id]
        return state.voice_sent and not state.video_offered

    def record_video_offered(self, user_id: int) -> None:
        self._states[user_id].video_offered = True
