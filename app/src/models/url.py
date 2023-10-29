from typing import Optional

from pydantic import BaseModel, AnyUrl


class UrlIn(BaseModel):

    incoming_link: AnyUrl

class UrlOut(BaseModel):

    scheme: str
    host: str
    username: Optional[str] = None
    password: Optional[str] = None
    port: Optional[int] = None
    path: Optional[str] = None
    query: Optional[str] = None
    fragment: Optional[str] = None