from database import Base
from sqlalchemy import Column,Integer,String,text,Date
from sqlalchemy.orm import Session
from schemas import Salida, OpcionesSalida, OpcionSalida,SolicitudesSalida
import schemas



class Opcion(Base):
    __tablename__='Opciones'
    idOpcion=Column(Integer,primary_key=True)
    nombre=Column(String,nullable=False)
    descripcion=Column(String)

    def consultar(self,db:Session):
       salida=OpcionesSalida()
       try:
           salida.estatus="OK"
           salida.mensaje="Listado de Opciones"
           salida.opciones=db.query(Opcion).all()
       except:
           salida.estatus="Error"
           salida.mensaje="Error al consultar las opciones"
           salida.opciones=[]
       return salida.dict()


    def agregar(self,db:Session):
        salida=Salida()
        try:
            db.add(self)
            db.commit()
            salida.estatus="OK"
            salida.mensaje="Opcion agregada con exito."
        except:
            salida.estatus="Error"
            salida.mensaje="Error al agregar la opcion"
        return salida.dict()
    def consultarPorId(self,id:int,db:Session):
        salida=OpcionSalida()
        try:
            salida.opcion=db.query(Opcion).filter(Opcion.idOpcion==id).first()
            salida.estatus = "OK"
            if salida.opcion:
                salida.mensaje="Listado de la opcion"
            else:
                salida.mensaje="La opcion no existe"
        except:
            salida.estatus="Error"
            salida.mensaje="Error al consultar la opcion"
            salida.opcion=None
        return salida.dict()
    def modificar(self,db:Session):
        salida=Salida()
        opcion=db.query(Opcion).filter(Opcion.idOpcion==self.idOpcion).first()
        if opcion:
            opcion.nombre=self.nombre
            opcion.descripcion=self.descripcion
            db.commit()
            db.refresh(opcion)
            salida.estatus="OK"
            salida.mensaje="Opcion modificada con exito"
        else:
            salida.estatus="OK"
            salida.mensaje="La opcion no existe"
        return salida.dict()
    def eliminar(self,id:int,db:Session):
        salida=Salida()
        try:
            opcion=db.query(Opcion).filter(Opcion.idOpcion==id).first()
            db.delete(opcion)
            db.commit()
            salida.estatus="OK"
            salida.mensaje="Opcion eliminada con exito"
        except:
            salida.estatus="Error"
            salida.mensaje="Error al eliminar la opcion"
        return salida.dict()
class Solicitud(Base):
    __tablename__='vSolicitudes'
    idSolicitud=Column(Integer,primary_key=True)
    tema=Column(String(300),nullable=False)
    idOpcion=Column(Integer)
    idAlumno=Column(Integer)
    noControl=Column(String(9))
    Alumno=Column(String)
    fechaRegistro=Column(Date)
    fechaAtencion=Column(Date)
    estatus=Column(String)
    Opcion=Column(String)
    idAdministrativo=Column(Integer)
    Coordinador=Column(String)
    idCarrera=Column(Integer)
    Carrera=Column(String)

    def registrar(self,db):
        datos_entrada={"p_tema":self.tema,"p_idOpcion":self.idOpcion,"p_idAlumno":self.idAlumno}
        db.execute(text('call sp_registrar_solicitud(:p_tema,:p_idOpcion,:p_idAlumno,@p_estatus,@p_mensaje)'),
                   datos_entrada)
        db.commit()
        respuesta=db.execute(text('select @p_estatus,@p_mensaje')).fetchone()
        salida=Salida()
        salida.estatus=respuesta[0]
        salida.mensaje=respuesta[1]
        return salida.dict()
    def consultar(self,db:Session):
        salida=SolicitudesSalida()

        lista=db.query(Solicitud).all()
        listaSolicitudes=[]
        for s in lista:
            objSol=self.to_schema(s)
            listaSolicitudes.append(objSol)
        salida.solicitudes=listaSolicitudes
        salida.estatus='OK'
        salida.mensaje='Listado de Solicititudes'

        return salida.dict()
    def to_schema(self,objeto):
        solicitud=schemas.SolicitudSelect()
        administrativo=schemas.Administrativo()
        administrativo.idAdministrativo=objeto.idAdministrativo
        administrativo.nombre=objeto.Coordinador
        solicitud.administrativo=administrativo
        #solicitud.administrativo.nombre = objeto.Coordinador
        alumno=schemas.Alumno()
        alumno.idAlumno=objeto.idAlumno
        alumno.nombre = objeto.Alumno
        alumno.noControl = objeto.noControl
        solicitud.alumno=alumno
        carrera=schemas.Carrera()
        carrera.idCarrera=objeto.idCarrera
        carrera.nombre=objeto.Carrera
        solicitud.carrera=carrera
        opcion=schemas.OpcionSolicitud()
        opcion.idOpcion=objeto.idOpcion
        opcion.nombre=objeto.Opcion
        solicitud.opcion=opcion
        solicitud.estatus=objeto.estatus
        solicitud.fechaAtencion=objeto.fechaAtencion
        solicitud.fechaRegistro=objeto.fechaRegistro
        solicitud.idSolicitud=objeto.idSolicitud
        solicitud.tema=objeto.tema
        return solicitud
        