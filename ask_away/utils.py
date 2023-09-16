import os
from typing import Optional

LANG_BADGES = {
    "python":     "[blue b]{}[/blue b]",
    "py":         "[blue b]{}[/blue b]",
    "html":       "[yellow b]{}[/yellow b]",
    "css":        "[green b]{}[/green b]",
    "javascript": "[cyan b]{}[/cyan b]",
    "js":         "[cyan b]{}[/cyan b]",
    "powershell": "[blue b]{}[/blue b]",
    "ps":         "[blue b]{}[/blue b]",
}

REGULAR_CMDS = (
    "run",
    "copy",
    "retry",
    "exit"
)

def get_badge(language: str) -> Optional[str]:
    lang = language.lower()
    return None if lang not in LANG_BADGES else (
        LANG_BADGES[lang].format("● " + language)
    )

def get_commands(*, without_run: bool = False):
    _cmds = REGULAR_CMDS[int(without_run):]
    return " • ".join(f"[u blue]/{cmd}[/u blue]" for cmd in _cmds)

def isreplit() -> bool:
    """The most basic way to detect whether this is a Replit environment or not."""
    env = os.environ

    return all((
        env.get("REPL_OWNER"),
        env.get("REPL_OWNER_ID"),
        env.get("REPL_ID"),
        env.get("REPL_SLUG")
    ))
