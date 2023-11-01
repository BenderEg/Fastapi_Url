from datetime import datetime, UTC
from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from core.config import settings
from models.url import UrlIn
from services.dependencies import url_service

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get('/', status_code=HTTPStatus.OK, response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse("main_page.html", {"request": request})


@router.post('/create/', status_code=HTTPStatus.CREATED)
async def create_url(link: UrlIn, url_service: url_service):

    link = str(link.incoming_link)
    hashed_link = await url_service.hash_link(link)
    check_storage = await url_service.get_from_storage(key=hashed_link)
    if check_storage:
        return f'{settings.domain}/{check_storage}'
    current_time = datetime.now(tz=UTC)
    uploaded_link = url_service.create_short_url(current_time)
    await url_service.add_url_to_storage(name=uploaded_link,
                                         values={'value': link,
                                                'counter': 0})
    await url_service.add_original_url_to_storage(hashed_link,
                                                  uploaded_link,
                                                  settings.cache)
    return f'{settings.domain}/{uploaded_link}'


@router.get('/{link}/', status_code=HTTPStatus.OK)
async def redirect_url(request: Request, link: str, url_service: url_service):
    link_in = link[:-1] if link[-1] == '+' else link
    link_out = await url_service.get_url_from_storage(name=link_in,
                                                      key='value')
    counts = int(await url_service.get_url_from_storage(name=link_in,
                                                    key='counter'))
    if not link_out:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="link doesn't exist in database.")
    if link[-1] == '+':
        return templates.TemplateResponse("counts.html",
                                          {"counts": counts,
                                           "link": link_out,
                                           "request": request})
    counts += 1
    await url_service.add_url_to_storage(name=link_in,
                                         values={'value': link_out,
                                                'counter': counts})
    return RedirectResponse(url=link_out,
                            status_code=HTTPStatus.MOVED_PERMANENTLY)