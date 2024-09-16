from flask import Flask,render_template,session,redirect,url_for,flash,request
from flask_bootstrap import Bootstrap

import ClientesServicios
from ClientesServicios import autenticar,consultarOpciones,agregarSolicitud,consultarSolicitud,actualizarSolicitud
app=Flask(__name__)
Bootstrap(app)
app.secret_key='MyCla4ve'
@app.route('/')
def index():
    return render_template('usuarios/login.html')
@app.route('/principal')
def principal():
    return render_template('comunes/principal.html')
@app.route('/login',methods=['post'])
def login():
    username=request.form['email']
    password=request.form['password']
    salida=autenticar(username,password)
    print(salida)
    if salida['estatus']=='OK':
        usuario=salida['usuario']
        session['usuario']=usuario
        return render_template('comunes/principal.html')
    else:
        flash(salida['mensaje'])
        return redirect(url_for('index'))
@app.route('/solicitudes',methods=['get'])
def consultarSolicitudes():
    usuario=session['usuario']
    salida=ClientesServicios.consultarSolicitudes(usuario)
    return render_template('solicitudes/listar.html',solicitudes=salida['solicitudes'])
@app.route('/solicitudes/nueva',methods=['get'])
def nuevaSolicitud():
    opciones=consultarOpciones()
    return render_template('solicitudes/crear.html',opciones=opciones)
@app.route('/solicitudes/editar/<int:id>')
def verSolicitud(id):
    opciones = consultarOpciones()
    salida= consultarSolicitud(id,session['usuario'])
    return render_template('solicitudes/editar.html',opciones=opciones,solicitud=salida['solicitud'])
@app.route('/solicitudes/registrar',methods=['post'])
def registrarSolicitud():
    datos={"tema":request.form['tema'],
           "idOpcion":request.form['idOpcion'],
           "idAlumno":session['usuario'].get('id')
           }
    salida=agregarSolicitud(datos,session['usuario'])
    flash(salida['mensaje'])
    return redirect(url_for('consultarSolicitudes'))
@app.route('/solicitudes/modificar',methods=['post'])
def modificarSolicitud():
    datos={"tema":request.form['tema'],
           "idOpcion":request.form['idOpcion'],
           "idAlumno":session['usuario'].get('id'),
           "idSolicitud":request.form['idSolicitud']}
    salida=actualizarSolicitud(datos,session['usuario'])
    flash(salida['mensaje'])
    return redirect(url_for('consultarSolicitudes'))
@app.route('/solicitudes/enviar/<int:idSolicitud>')
def enviarSolicitud(idSolicitud):
    datos={"idSolicitud":idSolicitud,
           "idAlumno":session['usuario'].get('id')}
    salida=ClientesServicios.enviarSolicitud(datos,session['usuario'])
    flash(salida['mensaje'])
    return redirect(url_for('consultarSolicitudes'))
@app.route('/solicitudes/cancelar/<int:idSolicitud>')
def cancelarSolicitud(idSolicitud):
    datos={"idSolicitud":idSolicitud,
           "idAlumno":session['usuario'].get('id')}
    salida=ClientesServicios.cancelarSolicitud(datos,session['usuario'])
    flash(salida['mensaje'])
    return redirect(url_for('consultarSolicitudes'))
@app.route('/solicitudes/autorizar/<int:idSolicitud>')
def autorizar(idSolicitud):
    datos={"idSolicitud":idSolicitud,
           "idAdministrativo":session['usuario'].get('id'),
           "estatus":"Autorizada"
    }
    salida = ClientesServicios.revisarSolicitud(datos, session['usuario'])
    flash(salida['mensaje'])
    return redirect(url_for('consultarSolicitudes'))
@app.route('/solicitudes/rechazar/<int:idSolicitud>')
def rechazar(idSolicitud):
    datos={"idSolicitud":idSolicitud,
           "idAdministrativo":session['usuario'].get('id'),
           "estatus":"Rechazada"
    }
    salida = ClientesServicios.revisarSolicitud(datos, session['usuario'])
    flash(salida['mensaje'])
    return redirect(url_for('consultarSolicitudes'))
@app.route('/cerrarSesion')
def cerrarSesion():
    print(session['usuario'].get('nombre'))
    session['usuario']=None
    return redirect(url_for('index'))
if __name__=='__main__':
    app.run(debug=True)