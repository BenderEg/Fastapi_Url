from pydantic import BaseModel, AnyUrl


class UrlIn(BaseModel):

    incoming_link: AnyUrl