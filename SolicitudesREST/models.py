from database import Base
from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import Session

class Opcion(Base):
    __tablename__='Opciones'
    idOpcion=Column(Integer,primary_key=True)
    nombre=Column(String,nullable=False)
    descripcion=Column(String)

    def consultar(self,db:Session):
       return db.query(Opcion).all()