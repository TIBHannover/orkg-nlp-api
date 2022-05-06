from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.routers import annotate

app = FastAPI(title='ORKG-NLP-API')
app.include_router(annotate.router)


@app.get('/', response_class=HTMLResponse)
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