from typing import Annotated

from fastapi import Depends

from services.url import UrlService, get_url_service

url_service = Annotated[UrlService, Depends(get_url_service)]