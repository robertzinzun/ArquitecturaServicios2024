from pydantic import BaseModel,Field
from typing import List
from datetime import date
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

class SolicitudInsert(BaseModel):
    tema:str
    idOpcion:int
    idAlumno:int

class Administrativo(BaseModel):
    idAdministrativo:int|None=None
    nombre:str|None=None

class Alumno(BaseModel):
    idAlumno:int|None=None
    noControl:str|None=None
    nombre:str|None=None

class Carrera(BaseModel):
    idCarrera:int|None=None
    nombre:str|None=None
class OpcionSolicitud(BaseModel):
    idOpcion:int|None=None
    nombre:str|None=None
class SolicitudSelect(BaseModel):
    administrativo:Administrativo|None=None
    alumno:Alumno|None=None
    carrera:Carrera|None=None
    estatus:str|None=None
    fechaAtencion:date|None=None
    fechaRegistro:date|None=None
    idSolicitud:int|None=None
    opcion:OpcionSolicitud|None=None
    tema:str|None=None
class SolicitudesSalida(Salida):
    solicitudes:List[SolicitudSelect]|None=[]
class SolicitudSalida(Salida):
    solicitud:SolicitudSelect|None=None
class SolicitudUpdate(SolicitudInsert):
    idSolicitud:int

class SolicitudCE(BaseModel):
    idSolicitud:int
    idAlumno:int

class SolicitudRevisar(BaseModel):
    idSolicitud:int
    idAdministrativo:int
    estatus:str


class Usuario(BaseModel):
    idUsuario:int|None=None
    nombre:str|None=None
    email:str|None=None
    password:str|None=None
    estatus:str|None=None
    telefono:str|None=None
    tipo:str|None=None
    sexo:str|None=None
    id:int|None=None
class UsuarioSalida(Salida):
    usuario:Usuario|None=None