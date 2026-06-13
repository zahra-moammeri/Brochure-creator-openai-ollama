from pydantic import BaseModel


class BrochureRequest(BaseModel):
    company_name: str
    url: str


