from flask import Flask,render_template,session,redirect,url_for,flash
from flask_bootstrap import Bootstrap
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
    usuario={'nombre':'Roberto',"idAlumno":1,"tipo":'Alumno'}
    session['usuario']=usuario
    return render_template('comunes/principal.html')
@app.route('/solicitudes',methods=['get'])
def consultarSolicitudes():
    return render_template('solicitudes/listar.html')
@app.route('/solicitudes/nueva',methods=['get'])
def nuevaSolicitud():
    return render_template('solicitudes/crear.html')
@app.route('/solicitudes/editar/<int:id>')
def verSolicitud(id):
    print(id)
    return render_template('solicitudes/editar.html')
@app.route('/solicitudes/registrar',methods=['post'])
def registrarSolicitud():
    flash('Solicitud agregada con exito')
    return redirect(url_for('consultarSolicitudes'))
@app.route('/solicitudes/modificar',methods=['post'])
def modificarSolicitud():
    flash('Solicitud modificada con exito')
    return redirect(url_for('consultarSolicitudes'))
@app.route('/cerrarSesion')
def cerrarSesion():
    print(session['usuario'].get('nombre'))
    session['usuario']=None
    return redirect(url_for('index'))
if __name__=='__main__':
    app.run(debug=True)