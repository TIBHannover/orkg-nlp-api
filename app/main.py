# -*- coding: utf-8 -*-
from fastapi.responses import HTMLResponse

from app.app_factory import create_app

app = create_app()


@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
        <head>
            <title> ORKG NLP API</title>
        </head>
        <body>
            Welcome to the Open Research Knowledge Graph NLP API
        </body>
    </html>
    """
