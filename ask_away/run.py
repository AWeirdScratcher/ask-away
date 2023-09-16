import tempfile
import webbrowser
from contextlib import asynccontextmanager as acm
from tempfile import TemporaryFile as TempFile
from typing import Dict, List, Tuple

import fastapi
import uvicorn
from fastapi.responses import HTMLResponse

from .utils import isreplit

LangCodes = Dict[str, List[str]]

def run_html(lang_codes: LangCodes):
    if isreplit():
        @acm
        async def lifespan(_):
            print("running at: ...")
            yield
    
        app = fastapi.FastAPI(lifespan=lifespan)
    
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
            uvicorn.run(
                app, 
                host="0.0.0.0", 
                port=8080
            )
        except KeyboardInterrupt:
            print("quitting app...")
    else:
        with tempfile.NamedTemporaryFile(
            "w", 
            encoding="utf-8",
            suffix=".html"
        ) as file:
            file.write(lang_codes['html'][0])
            webbrowser.open_new_tab("file://" + file.name)

            try:
                input("Press CTRL+C to quit...")
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
        )

        if lang not in codes:
            codes[lang] = [code]
        else:
            codes[lang].append(code)


    if "html" in codes:
        run_html(codes)

