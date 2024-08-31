from pydantic import BaseModel

class Opcion(BaseModel):
    idOpcion:int|None=None
    nombre:str
    descripcion:str
    class Config:
        orm_mode=True

class OpcionInsert(BaseModel):
    nombre:str
    descripcion:str