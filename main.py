from ipaddress import ip_address
from typing import Callable
import time

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from redis.asyncio import Redis
from sqlalchemy import text
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware


from src.database.db import get_db
from src.routes import users, auth
from src.repository.users import get_user_by_email
from src.conf.config import settings

app = FastAPI()


@app.on_event("startup")
async def startup():
    r = await Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=0,
    )
    await FastAPILimiter.init(r)


app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/templates", StaticFiles(directory="templates"), name="templates")
templates = Jinja2Templates(directory="templates")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_IPS = [
    ip_address("192.168.1.0"),
    ip_address("192.168.2.0"),
    ip_address("127.0.0.1"),
]


@app.middleware("http")
async def limit_access_by_ip(request: Request, call_next: Callable):
    ip = ip_address(request.client.host)
    if ip not in ALLOWED_IPS:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "Not allowed IP address"},
        )
    response = await call_next(request)
    return response


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["My-Process-Time"] = str(process_time)
    return response


@app.get(
    "/",
    response_class=HTMLResponse,
    description="Main Page",
    dependencies=[Depends(RateLimiter(times=2, seconds=10))],
)
def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "title": "My App"}
    )


@app.get("/main.html", response_class=HTMLResponse, description="Main Page")
def read_root(request: Request):
    return templates.TemplateResponse(
        "main.html", {"request": request, "title": "My App"}
    )


@app.get(
    "/signup.html",
    response_class=HTMLResponse,
    description="Sign Up",
    dependencies=[Depends(RateLimiter(times=2, seconds=10))],
)
async def signup(request: Request):
    return templates.TemplateResponse(
        "signup.html", {"request": request, "title": "My App"}
    )


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
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
