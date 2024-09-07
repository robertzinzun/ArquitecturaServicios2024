from fastapi import FastAPI,Depends
import uvicorn
from schemas import OpcionInsert, Salida, OpcionesSalida, OpcionSalida, Opcion, SolicitudInsert,SolicitudesSalida
from database import get_db
#from models import Opcion
from sqlalchemy.orm import Session
from typing import Any
import models
app=FastAPI()

@app.get('/')
def home():
    return {"mensaje":"Bienvenido a SolicitudesREST"}
@app.get('/opciones',tags=["Consultar Opciones"],response_model=OpcionesSalida)
async def consultarOpciones(db:Session=Depends(get_db))->Any:
    #db=get_db()
    print(db)
    opcion=models.Opcion()
    return opcion.consultar(db)

@app.get('/opciones/{id}',tags=["Consultar Opcion"],response_model=OpcionSalida)
def consultarOpcion(id:int,db:Session=Depends(get_db)):
    opcion=models.Opcion()
    return opcion.consultarPorId(id,db)
@app.post('/opciones',tags=["Crear Opcion"],response_model=Salida)
def crearOpcion(opcionInsert:OpcionInsert,db:Session=Depends(get_db))->Any:
    #llamado a la operacion de la BD encargada de registrar el objeto
    opcion=models.Opcion(nombre=opcionInsert.nombre,descripcion=opcionInsert.descripcion)
    return opcion.agregar(db)


@app.put('/opciones',tags=["Modificar Opcion"],response_model=Salida)
def modificarOpcion(opcionU:Opcion,db:Session=Depends(get_db))->Any:
    op=models.Opcion(idOpcion=opcionU.idOpcion,
                     nombre=opcionU.nombre,
                     descripcion=opcionU.descripcion)
    return op.modificar(db)

@app.delete("/opciones/{id}",tags=["Eliminar Opcion"],response_model=Salida)
def eliminarOpcion(id:int,db:Session=Depends(get_db))->Any:
    opcion=models.Opcion()
    return opcion.eliminar(id,db)

@app.post('/solicitudes',tags=["Registrar Solicitud"],response_model=Salida)
def agregarSolicitud(solicitudI:SolicitudInsert,db:Session=Depends(get_db))->Any:
    solicitud=models.Solicitud(tema=solicitudI.tema,idOpcion=solicitudI.idOpcion,
                               idAlumno=solicitudI.idAlumno)
    return solicitud.registrar(db)

@app.get('/solicitudes',tags=["Consultar Solicitudes"],response_model=SolicitudesSalida)
def consultarSolicitudes(db:Session=Depends(get_db))->Any:
    solicitud=models.Solicitud()
    return solicitud.consultar(db)

if __name__=="__main__":
    uvicorn.run("main:app", host="127.0.0.1", reload=True)