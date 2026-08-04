"""GroundedChatWidget — renders GroundedChatViewModel list + chat input."""

from __future__ import annotations

from textual.containers import Vertical
from textual.widgets import ListView, ListItem, Input, Static

from jarvis.presentation.viewmodels import GroundedChatViewModel

class GroundedChatWidget(Vertical):
    """Combined chat widget: conversation log + query input.

    Renders GroundedChatViewModel responses and provides query submission.
    """

    def compose(self) -> None:
        """Create child widgets: chat log list + input field."""
        yield ListView(id="chat_log")
        yield Input(placeholder="Ask a question about findings…", id="chat-input")

    def update_view_model(self, responses: tuple[GroundedChatViewModel, ...]) -> None:
        """Render chat responses from an immutable view model list."""
        log = self.query_one("#chat-log", ListView)
        log.clear()
        if not responses:
            log.append(ListItem("No chat responses yet."))
            return
        for resp in responses:
            label = f"Q: {resp.query_text} | A: {resp.rendered_markdown[:80]}..."
            log.append(ListItem(label))