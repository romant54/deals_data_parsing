from pydantic import BaseModel

class PreprocessingDealSchema(BaseModel):
    id: int
    data: dict

    class Config:
        orm_mode = True

class DealSchema(BaseModel):
    id: int
    data: dict

    class Config:
        orm_mode = True
