from pydantic import BaseModel


class NanozymesBotRequest(BaseModel):
    query_text: str
    instruction: str
    context: str
    article: dict


class NanozymesBotResponse(BaseModel):
    answer: str
    context: str
