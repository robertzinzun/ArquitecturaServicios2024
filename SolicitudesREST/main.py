from fastapi import FastAPI,Depends
import uvicorn
from schemas import OpcionInsert
from database import get_db
from models import Opcion
from sqlalchemy.orm import Session
app=FastAPI()

@app.get('/')
def home():
    return {"mensaje":"Bienvenido a SolicitudesREST"}
@app.get('/opciones',tags=["Consultar Opciones"])
async def consultarOpciones(db:Session=Depends(get_db)):
    #db=get_db()
    print(db)
    opcion=Opcion()
    return opcion.consultar(db)
    #return {"mensaje":"Consultando opciones"}
@app.get('/opciones/{id}',tags=["Consultar Opcion"])
def consultarOpcion(id:int):
    return {"mensaje":f"Consultando opcion con {id}"}
@app.post('/opciones',tags=["Crear Opcion"])
def crearOpcion(opcion:OpcionInsert):
    return {"mensaje":"Registrando Opcion",
            "opcion":opcion}
@app.put('/opciones',tags=["Modificar Opcion"])
def modificarOpcion():
    return {"mensaje":"Modificando Opcion"}
@app.delete("/opciones",tags=["Eliminar Opcion"])
def eliminarOpcion():
    return {"mensaje":"Eliminando Opcion"}

#if __name__=="__main__":
#    uvicorn.run(app=app,reload=True)