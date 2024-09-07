from pydantic import BaseModel,Field
from typing import List

class Opcion(BaseModel):
    idOpcion:int
    nombre:str
    descripcion:str
    class Config:
        orm_mode=True

class OpcionInsert(BaseModel):
    nombre:str
    descripcion:str

class Salida(BaseModel):
    estatus:str=Field(default="")
    mensaje:str=Field(default="")

class OpcionesSalida(Salida):
    opciones:List[Opcion]|None=[]

class OpcionSalida(Salida):
    opcion:Opcion|None=None