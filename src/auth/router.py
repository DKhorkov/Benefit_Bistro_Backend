from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from src.config import PathsConfig, PageNamesConfig


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

# Mounts:
templates = Jinja2Templates(directory=PathsConfig.TEMPLATES.__str__())


@router.get('/register', response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse(
        name=PathsConfig.REGISTER_PAGE.__str__(),
        request=request,
        context={'title': PageNamesConfig.REGISTER_PAGE},
    )


@router.get('/login', response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse(
        name=PathsConfig.LOGIN_PAGE.__str__(),
        request=request,
        context={'title': PageNamesConfig.LOGIN_PAGE},
    )