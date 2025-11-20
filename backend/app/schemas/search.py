from pydantic import BaseModel

class SearchResult(BaseModel):
    id: str
    text: str
    type: str