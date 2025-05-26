import os
from math import trunc

import uvicorn
from starlette.staticfiles import StaticFiles

from base import get_app
from base.routes.api_routes import router as api_router

app = get_app()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
