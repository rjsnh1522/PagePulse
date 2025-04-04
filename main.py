# fmt: off
from dotenv import load_dotenv
load_dotenv('.env')
# fmt: on
from starlette.middleware.cors import CORSMiddleware

from utils.app_logger import createLogger
from api import routes
from fastapi.routing import APIRoute
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse



# from utils.app_helper import validation_exception_handler

logger = createLogger("app")


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0] if route.tags else ['abcd']}-{route.name}"



# Define allowed origins (Replace with your actual blog URL)
allowed_origins = [
    "https://rjsnh1522.github.io/",  # Your blog
    "https://rjsnh1522.github.io",  # Your blog
    "http://localhost:1313/",
    "http://localhost:1313",

]


app = FastAPI(
    title="PagePulse",
    generate_unique_id_function=custom_generate_unique_id
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Allow specific domains
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", name="root")
async def root(request: Request):
    logger.info("Some message")
    return "True"


@app.options("/{full_path:path}")
async def preflight_handler(request: Request, full_path: str):
    return JSONResponse(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
    )

app.include_router(routes.api_router, prefix="/v1")
