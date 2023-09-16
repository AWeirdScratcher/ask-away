import os
import warnings
from typing import Iterator

import pyperclip
from rich.console import Console
from rich.markdown import Markdown

from .detect_lang import detect_lang_code
from .providers import free_ask
from .run import run_code
from .stream import Stream
from .utils import get_badge, get_commands

console = Console()

def ask(
    messages, 
    *, 
    disable_streaming: bool = False
) -> str:
    here = os.path.dirname(__file__)
    with open(
        os.path.join(here, "prompt.txt"), 
        "r", 
        encoding='utf-8'
    ) as f:
        prompt = f.read()

    def _execute() -> Iterator[str]:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore") # tz warnings
    
            for chunk in free_ask([
                {
                    "role": "system", 
                    "content": prompt
                },
                *messages
            ]):
                yield chunk

    if disable_streaming:
        f = ""
        with console.status("✨ Generating..."):
            for chunk in _execute():
                f += chunk

        console.print(Markdown(
            f,
            code_theme="one-dark"
        ))

        return f

    stream = Stream(console)

    for chunk in _execute():
        stream.edit(chunk)

    stream.done()
    return stream.f

def print_runnables(lang_codes) -> None:
    languages = set()

    for lang, _ in lang_codes:
        bdg = get_badge(lang)
        if bdg:
            languages.add(bg)

    if not languages:
        return

    console.print(
        "[d white]runnables:[/d white]\n",
    )

    for lang in languages:
        if lang:
            console.print(" ", lang, end=" ")

    console.print("\n")


def cli():
    messages = []

    console.print()
    console.print(
        "  [green]ask-away[/green] alpha\n"
    )
    console.print(
        "  How can I assist you today?\n"
    )
    console.print(
        "\n[d white]pro tip: "
        "use --wait to at the end to disable streaming[/d white]"
    )
    files = []

    while True:
        query = input("\n>>> ").strip()
        if not query:
            continue

        addons = "..."
        while addons and not query.startswith('/'):
            addons = input("... ").strip()
            query += (
                "\n" + addons
            ) if addons else ""

        if query.startswith("/"):
            if query == "/copy" and messages:
                try:
                    pyperclip.copy(messages[-1]['content'])
                except pyperclip.PyperclipException:
                    console.print(
                        "[red]cannot copy programmatically, please select & copy[/red]"
                    )
                    console.print()
                    console.print(
                        messages[-1]['content']
                    )

                continue

            elif query == "/run" and files:
                console.print("[blue]running...[/blue]")
                run_code(files)

            else:
                console.print("Unrecognized command or bad usage")
                continue

        disable_streaming = query.endswith("--wait")

        if disable_streaming:
            query = query[len("--wait"):].strip()

            if not query:
                continue

        console.print()
        messages.append({
            "role": "user",
            "content": query
        })
        response = ask(messages, disable_streaming=disable_streaming)
        messages.append({
            "role": "assistant",
            "content": response
        })
        lang_codes = detect_lang_code(response)
        print_runnables(lang_codes)
        files = lang_codes
        
        console.print(
            "[d white]commands:[/d white]",
            get_commands(
                without_run=(not lang_codes)
            )
        )
    
