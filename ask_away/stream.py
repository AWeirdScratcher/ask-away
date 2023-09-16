from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel


class Stream:
    def __init__(self, console: Console):
        self.f = ""
        self.cursor = "█"
        self.md = Markdown(self.cursor, code_theme="one-dark")
        self.live = Live(self.md, console=console)
        self.live.start()

    def edit(self, chunk: str):
        self.f += chunk
        self._update()

    def done(self):
        self._update(cursor=False)
        self.live.stop()

    def _update(self,  *, cursor: bool = True):
        self.md = Markdown(
            self.f + (self.cursor if cursor else ""),
            code_theme="one-dark"
        )
        self.live.update(
            Panel(
                self.md,
                title="✨ ChatGPT",
                title_align="left"
            )
        )
        self.live.refresh()

