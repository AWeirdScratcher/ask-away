import os
import socket
import webbrowser
from contextlib import asynccontextmanager as acm
from tempfile import TemporaryFile as TempFile
from typing import Dict, List, Tuple

import fastapi
import uvicorn
from fastapi.responses import HTMLResponse
from rich import print as rprint

from .utils import isreplit

LangCodes = Dict[str, List[str]]

def run_html(lang_codes: LangCodes):
    isReplit: bool = isreplit()

    app = fastapi.FastAPI()

    @app.get("/")
    async def index():
        return HTMLResponse(
            lang_codes["html"][0]
        )

    @app.get("/styles.css")
    async def css():
        return "\n".join(
            lang_codes.get("css", [])
        )

    @app.get("/scripts.js")
    async def js():
        return "\n".join(
            lang_codes.get("js", [])
        )

    try:
        if isReplit:
            @acm
            async def replit_lifespan(_):
                rprint()
                pos = (
                    f"https://{os.environ['REPL_SLUG']}."
                    f"{os.environ['REPL_OWNER']}.repl.co"
                )
                rprint(f"  🔥 running at: {pos}\n")
                yield
    
            app.router.lifespan_context = replit_lifespan # monke
            uvicorn.run(
                app, 
                host="0.0.0.0",
                port=8080
            )

        else:
            # https://stackoverflow.com/questions/1365265/on-localhost-how-do-i-pick-a-free-port-number
            sock = socket.socket()
            sock.bind(('', 0))
            sockname = sock.getsockname()

            @acm
            async def local_lifespan(_):
                rprint()
                rprint(f"  🔥 running at: http://localhost:{sockname[1]}\n")
                webbrowser.open(f"http://localhost:{sockname[1]}")
                yield
            
            app.router.lifespan_context = local_lifespan # monke

            uvicorn.run(
                app,
                port=sockname[1]
            )
    
    except KeyboardInterrupt:
        print("quitting app...")

RUN_METHODS = {
    "python": {
        "exec": ...
    },
    "html": {
        "exec": run_html
    }
}
TRANSFORM = {
    "javascript": "js"
}

def run_code(lang_codes: List[Tuple[str, str]]):
    codes = {}

    for _lang, code in lang_codes:
        lang = TRANSFORM.get(
            _lang,
            _lang
        ).lower()

        if lang not in codes:
            codes[lang] = [code]
        else:
            codes[lang].append(code)


    if "html" in codes:
        run_html(codes)

