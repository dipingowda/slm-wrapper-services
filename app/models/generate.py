from pydantic import BaseModel,Field


class GenerateRequest(BaseModel):
    prompt:str
    model:str = Field(default="phi3:mini",description="The model to use for generation") 

class GenerateResponse(BaseModel):
    prompt:str
    model:str
    response:str