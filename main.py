
from utils.app_logger import createLogger
from api import routes
from fastapi.routing import APIRoute
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from dotenv import load_dotenv
load_dotenv('.env')


# from utils.app_helper import validation_exception_handler


logger = createLogger("app")


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0] if route.tags else ['abcd']}-{route.name}"


app = FastAPI(
    title="PagePulse",
    generate_unique_id_function=custom_generate_unique_id
)


@app.get("/", name="root")
async def root(request: Request):
    logger.info("Some message")
    return "True"


app.include_router(routes.api_router, prefix="/v1")
