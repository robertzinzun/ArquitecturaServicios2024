import requests
from requests.auth import HTTPBasicAuth

def autenticar(username,password):
    url='http://localhost:8000/usuarios/autenticar'
    credenciales=HTTPBasicAuth(username,password)
    respuesta=requests.get(url,auth=credenciales)
    return respuesta.json()
def consultarOpciones():
    url='http://127.0.0.1:8000/opciones'
    respuesta=requests.get(url)
    salida=respuesta.json()
    if salida['estatus']=='OK':
        return salida['opciones']
    else:
        return salida
def consultarSolicitudes(usuario):
    if usuario['tipo']=='Alumno':
        url=f'http://127.0.0.1:8000/solicitudes/alumno/{usuario['id']}'
    else:
        if usuario['tipo']=='Administrativo':
            url = f'http://127.0.0.1:8000/solicitudes/coordinador/{usuario['id']}'
        else:
            url='http://127.0.0.1:8000/solicitudes'

    credenciales = HTTPBasicAuth(usuario['email'], usuario['password'])
    respuesta=requests.get(url,auth=credenciales)
    return respuesta.json()
def agregarSolicitud(entrada,usuario):
    url='http://127.0.0.1:8000/solicitudes'
    credenciales=HTTPBasicAuth(usuario['email'], usuario['password'])
    respuesta=requests.post(url,auth=credenciales,json=entrada).json()
    return respuesta

def consultarSolicitud(id,usuario):
    url=f'http://127.0.0.1:8000/solicitudes/{id}'
    credenciales = HTTPBasicAuth(usuario['email'], usuario['password'])
    respuesta = requests.get(url, auth=credenciales).json()
    return respuesta
def actualizarSolicitud(entrada,usuario):
    url = 'http://127.0.0.1:8000/solicitudes'
    credenciales = HTTPBasicAuth(usuario['email'], usuario['password'])
    respuesta = requests.put(url, auth=credenciales,json=entrada).json()
    print(respuesta)
    return respuesta
def enviarSolicitud(entrada,usuario):
    url = f'http://127.0.0.1:8000/solicitudes/enviar'
    credenciales = HTTPBasicAuth(usuario['email'], usuario['password'])
    respuesta = requests.put(url, auth=credenciales, json=entrada).json()
    return respuesta
def cancelarSolicitud(entrada,usuario):
    url = f'http://127.0.0.1:8000/solicitudes/cancelar'
    credenciales = HTTPBasicAuth(usuario['email'], usuario['password'])
    respuesta = requests.delete(url, auth=credenciales, json=entrada).json()
    return respuesta
def revisarSolicitud(entrada,usuario):
    url = f'http://127.0.0.1:8000/solicitudes/revisar'
    credenciales = HTTPBasicAuth(usuario['email'], usuario['password'])
    respuesta = requests.put(url, auth=credenciales, json=entrada)
    salida=respuesta.json()
    return salida