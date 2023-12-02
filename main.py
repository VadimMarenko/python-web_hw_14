# from ipaddress import ip_address
# from typing import Callable
from pathlib import Path
import time

from fastapi import FastAPI, Depends, HTTPException, status, Request

from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import redis.asyncio as redis
from sqlalchemy import text
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware


from src.database.db import get_db
from src.routes import users, auth
from src.conf.config import settings

app = FastAPI()

BASE_DIR = Path(__file__).parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.mount("/templates", StaticFiles(directory=BASE_DIR / "templates"), name="templates")
templates = Jinja2Templates(directory="templates")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ALLOWED_IPS = [
#     ip_address("192.168.1.0"),
#     ip_address("192.168.2.0"),
#     ip_address("127.0.0.1"),
# ]


# @app.middleware("http")
# async def limit_access_by_ip(request: Request, call_next: Callable):
#     """
#     The limit_access_by_ip function is a middleware that limits access to the API by IP address.
#     It checks if the client's IP address is in ALLOWED_IPS, and if not, it returns an error message.

#     :param request: Request: Get the client's ip address
#     :param call_next: Callable: Pass the next function in the pipeline
#     :return: A jsonresponse object with a status code of 403 and a detail message
#     :doc-author: Trelent
#     """
#     ip = ip_address(request.client.host)
#     if ip not in ALLOWED_IPS:
#         return JSONResponse(
#             status_code=status.HTTP_403_FORBIDDEN,
#             content={"detail": "Not allowed IP address"},
#         )
#     response = await call_next(request)
#     return response


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    The add_process_time_header function is a middleware function that adds a header to the response,
    which contains the time it took for FastAPI to process the request.


    :param request: Request: Access the request object
    :param call_next: Call the next middleware in the chain
    :return: A response object
    :doc-author: Trelent
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["My-Process-Time"] = str(process_time)
    return response


@app.on_event("startup")
async def startup():
    """
    The startup function is called when the application starts up.
    It can be used to initialize resources, such as database connections.

    :return: A coroutine, so we need to run it:
    :doc-author: Trelent
    """
    r = await redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=0,
    )
    await FastAPILimiter.init(r)


@app.get(
    "/",
    response_class=HTMLResponse,
    description="Main Page",
    # dependencies=[Depends(RateLimiter(times=2, seconds=10))],
)
def read_root(request: Request):
    """
    The read_root function is a FastAPI path operation that returns an HTMLResponse object.
    The HTMLResponse object contains the rendered template, which in this case is index.html.

    :param request: Request: Pass the request object to the template
    :return: A templateresponse object
    :doc-author: Trelent
    """
    return templates.TemplateResponse(
        "index.html", {"request": request, "title": "My App"}
    )


@app.get("/main.html", response_class=HTMLResponse, description="Main Page")
def read_root(request: Request):
    """
    The read_root function is a view function that returns an HTML response.
    The HTML response is generated by the main.html template, which uses the title variable to set the page title.

    :param request: Request: Tell fastapi that the parameter is a request object
    :return: A templateresponse object
    :doc-author: Trelent
    """
    return templates.TemplateResponse(
        "main.html", {"request": request, "title": "My App"}
    )


@app.get(
    "/signup.html",
    response_class=HTMLResponse,
    description="Sign Up",
    # dependencies=[Depends(RateLimiter(times=2, seconds=10))],
)
async def signup(request: Request):
    """
    The signup function handles the signup form submission.
    It creates a new user and saves it to the database.

    :param request: Request: Access the request object
    :return: A templateresponse object, which is a subclass of response
    :doc-author: Trelent
    """
    return templates.TemplateResponse(
        "signup.html", {"request": request, "title": "My App"}
    )


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    """
    The healthchecker function is a simple function that checks the health of the database.
    It does this by making a request to the database and checking if it returns any results.
    If there are no results, then we know something is wrong with our connection to the database.

    :param db: Session: Get the database session
    :return: The message &quot;welcome to fastapi!&quot;
    :doc-author: Trelent
    """
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()
        print(result)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database is not configured correctly",
            )
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error connecting to the database",
        )


app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
