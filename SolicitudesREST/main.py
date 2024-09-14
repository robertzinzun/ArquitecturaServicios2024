from fastapi import FastAPI,Depends,HTTPException,status
import uvicorn
from schemas import OpcionInsert, Salida, OpcionesSalida, OpcionSalida, Opcion, SolicitudInsert, SolicitudesSalida, \
    SolicitudUpdate, SolicitudCE, SolicitudRevisar, SolicitudSalida,UsuarioSalida
from database import get_db
#from models import Opcion
from sqlalchemy.orm import Session
from typing import Any
import models
from fastapi.security import HTTPBasic,HTTPBasicCredentials
app=FastAPI()
security=HTTPBasic()
@app.get('/')
def home():
    return {"mensaje":"Bienvenido a SolicitudesREST"}
def autenticar(credenciales:HTTPBasicCredentials=Depends(security),
               db:Session=Depends(get_db))->UsuarioSalida:
    return models.autenticar(credenciales.username,credenciales.password,db)
@app.get('/opciones',tags=["Opciones"],summary="Consultar Opciones",response_model=OpcionesSalida)
async def consultarOpciones(db:Session=Depends(get_db))->Any:
    #db=get_db()
    print(db)
    opcion=models.Opcion()
    return opcion.consultar(db)

@app.get('/opciones/{idOpcion}',tags=["Opciones"],summary="Consultar Opcion",response_model=OpcionSalida)
def consultarOpcion(idOpcion:int,db:Session=Depends(get_db)):
    opcion=models.Opcion()
    return opcion.consultarPorId(idOpcion,db)
@app.post('/opciones',tags=["Opciones"],summary="Crear Opcion",response_model=Salida)
def crearOpcion(opcionInsert:OpcionInsert,db:Session=Depends(get_db))->Any:
    #llamado a la operacion de la BD encargada de registrar el objeto
    opcion=models.Opcion(nombre=opcionInsert.nombre,descripcion=opcionInsert.descripcion)
    return opcion.agregar(db)
@app.put('/opciones',tags=["Opciones"],summary="Modificar Opcion",response_model=Salida)
def modificarOpcion(opcionU:Opcion,db:Session=Depends(get_db))->Any:
    op=models.Opcion(idOpcion=opcionU.idOpcion,
                     nombre=opcionU.nombre,
                     descripcion=opcionU.descripcion)
    return op.modificar(db)
@app.delete("/opciones/{idOpcion}",tags=["Opciones"],summary="Eliminar Opcion",response_model=Salida)
def eliminarOpcion(idOpcion:int,db:Session=Depends(get_db))->Any:
    opcion=models.Opcion()
    return opcion.eliminar(idOpcion,db)
@app.post('/solicitudes',tags=["Solicitudes"],summary="Registrar Solicitud",response_model=Salida)
def agregarSolicitud(solicitudI:SolicitudInsert,db:Session=Depends(get_db),
                     salida:UsuarioSalida=Depends(autenticar))->Any:
    if salida.estatus=='OK' and salida.usuario.tipo=='Alumno':
        solicitud=models.Solicitud(tema=solicitudI.tema,idOpcion=solicitudI.idOpcion,
                               idAlumno=solicitudI.idAlumno)
        return solicitud.registrar(db)
    else:
        if salida.estatus=='OK':
            salida.estatus='Error'
            salida.mensaje='El usuario no tiene autorizacion'
            return salida.dict()
        else:
            return salida.dict()
@app.put('/solicitudes',tags=["Solicitudes"],summary="Modificar Solicitud",response_model=Salida)
def modificarSolicitud(s:SolicitudUpdate,db:Session=Depends(get_db),
                       salida:UsuarioSalida=Depends(autenticar))->Any:
    if salida.estatus == 'OK' and salida.usuario.tipo == 'Alumno':
        solicitud=models.Solicitud(idSolicitud=s.idSolicitud,idAlumno=s.idAlumno,
                               tema=s.tema,idOpcion=s.idOpcion)
        return solicitud.modificar(db)
    else:
        if salida.estatus=='OK':
            salida.estatus='Error'
            salida.mensaje='El usuario no tiene autorizacion'
            return salida.dict()
        else:
            return salida.dict()

@app.delete('/solicitudes/cancelar',tags=["Solicitudes"],summary='Cancelar Solicitud',response_model=Salida)
def cancelarSolicitud(s:SolicitudCE,db:Session=Depends(get_db),
                      salida:UsuarioSalida=Depends(autenticar))->Any:
    if salida.estatus == 'OK' and salida.usuario.tipo == 'Alumno':
        solicitud=models.Solicitud(idSolicitud=s.idSolicitud,idAlumno=s.idAlumno)
        return solicitud.cancelar(db)
    else:
        if salida.estatus=='OK':
            salida.estatus='Error'
            salida.mensaje='El usuario no tiene autorizacion'
            return salida.dict()
        else:
            return salida.dict()
@app.put('/solicitudes/enviar',tags=["Solicitudes"],summary="Enviar Solicitud",response_model=Salida)
def enviarSolicitud(s:SolicitudCE,db:Session=Depends(get_db),
                    salida:UsuarioSalida=Depends(autenticar))->Any:
    if salida.estatus == 'OK' and salida.usuario.tipo == 'Alumno':
        solicitud=models.Solicitud(idSolicitud=s.idSolicitud,idAlumno=s.idAlumno)
        return solicitud.enviar(db)
    else:
        if salida.estatus=='OK':
            salida.estatus='Error'
            salida.mensaje='El usuario no tiene autorizacion'
            return salida.dict()
        else:
            return salida.dict()
@app.put('/solicitudes/revisar',tags=["Solicitudes"],summary="Revisar Solicitud",response_model=Salida)
def revisarSolicitud(s:SolicitudRevisar,db:Session=Depends(get_db),
                     salida:UsuarioSalida=Depends(autenticar))->Any:
    if salida.estatus == 'OK' and salida.usuario.tipo == 'Administrativo':
        solicitud=models.Solicitud(idSolicitud=s.idSolicitud,
                                   idAdministrativo=s.idAdministrativo,
                                   estatus=s.estatus)
        return solicitud.revisar(db)
    else:
        if salida.estatus=='OK':
            salida.estatus='Error'
            salida.mensaje='El usuario no tiene autorizacion'
            return salida.dict()
        else:
            return salida.dict()
@app.get('/solicitudes',tags=["Solicitudes"],summary="Consultar Solicitudes",response_model=SolicitudesSalida)
def consultarSolicitudes(db:Session=Depends(get_db),
                         salida:UsuarioSalida=Depends(autenticar))->Any:

    if salida.estatus=='OK':
        solicitud=models.Solicitud()
        return solicitud.consultar(db)
    else:
        return salida.dict()

@app.get('/solicitudes/{idSolicitud}',tags=["Solicitudes"],summary="Consultar Solicitud",response_model=SolicitudSalida)
def consultarSolicitud(idSolicitud:int,db:Session=Depends(get_db),
                       salida:UsuarioSalida=Depends(autenticar))->Any:
    if salida.estatus == 'OK':
        solicitud=models.Solicitud()
        return solicitud.consultarPorId(db,idSolicitud)
    else:
        return salida.dict()
@app.get('/solicitudes/alumno/{idAlumno}',tags=["Solicitudes"],summary="Consultar Solicitudes por Alumno",response_model=SolicitudesSalida)
def consultarSolicitudesPorAlumno(idAlumno:int,db:Session=Depends(get_db),
                                  salida:UsuarioSalida=Depends(autenticar))->Any:
    if salida.estatus == 'OK' and salida.usuario.tipo == 'Alumno':
        solicitud=models.Solicitud()
        return solicitud.consultarPorAlumno(db,idAlumno)
    else:
        if salida.estatus=='OK':
            salida.estatus='Error'
            salida.mensaje='El usuario no tiene autorizacion'
            return salida.dict()
        else:
            return salida.dict()
@app.get('/solicitudes/coordinador/{idCoordinador}',tags=["Solicitudes"],summary="Consultar Solicitudes por Coordinador",response_model=SolicitudesSalida)
def consultarSolicitudesPorCoodinador(idCoordinador:int,db:Session=Depends(get_db),
                                      salida:UsuarioSalida=Depends(autenticar))->Any:
    if salida.estatus == 'OK' and salida.usuario.tipo == 'Administrativo':
        solicitud=models.Solicitud()
        return solicitud.consultarPorCoordinador(db,idCoordinador)
    else:
        if salida.estatus=='OK':
            salida.estatus='Error'
            salida.mensaje='El usuario no tiene autorizacion'
            return salida.dict()
        else:
            return salida.dict()



@app.get('/usuarios/autenticar',tags=["Usuarios"],
         summary='Autenticacion de un Usuario',response_model=UsuarioSalida)
def login(usuario:UsuarioSalida=Depends(autenticar))->Any:
    return usuario
if __name__=="__main__":
    uvicorn.run("main:app", host="127.0.0.1", reload=True)