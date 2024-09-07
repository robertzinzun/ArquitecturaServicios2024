from database import Base
from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import Session
from schemas import Salida, OpcionesSalida, OpcionSalida



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

