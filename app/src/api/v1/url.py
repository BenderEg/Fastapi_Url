from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from models.url import UrlIn, UrlOut
from services.dependencies import url_service

router = APIRouter(prefix='/url')

@router.post('/create', status_code=HTTPStatus.OK,
             response_model=UrlOut)
async def create_url(link: UrlIn, url_service: url_service):
    link_out = UrlOut(scheme=link.incoming_link.scheme,
                  host=link.incoming_link.host,
                  path=link.incoming_link.path,
                  query=link.incoming_link.query)
    uploaded_link = url_service.create_short_url(link_out)
    await url_service.add_url_to_storage(key=uploaded_link, value=str(link.incoming_link))
    return link_out


@router.post('/forward', status_code=HTTPStatus.OK)
async def redirect_url(body: dict, url_service: url_service):
    link_out= await url_service.get_url_from_storage(key=body.get('link'))
    if not link_out:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail="link doesn't exist in database.")
    return {'link': link_out}