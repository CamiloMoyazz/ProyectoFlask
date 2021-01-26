import os

from flask import Flask

#Aqui creamos la app osea , nuestra instancia de flask en la que vivirá nuesta pagina web

#Luego de crear todas las instrucciones y las conecciones respectivas a la DB
#debemos exportar los datos de coneccion de la BASE de datos para que servena reflejados abajo en FLASK_DATABASE_HOST,PASSWORD,USER,
#Como lo hacemos, vamos a nuestra terminal entramos hasta la carpeta general del proyecyo
# y escrimimos tal cual
# export FLASK_DATABASE_HOST='nombre del host' ENTER
# export FLASK_DATABASE_PASSWORD='password' ENTER
# export FLASK_DATABASE_USER='nombre user' ENTER
# export FLASK_DATABASE='nombre de la BD'

#Finalmente para comprobar que todo funciona bien, vamos hasta la terminal para ejecutar la funcion init_command que nosotros hayamos creado
# para de esa forma sepamos que la coneccion se realizo con exito

def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY ='mikey',
        DATABASE_HOST=os.environ.get('FLASK_DATABASE_HOST'),
        DATABASE_PASSWORD=os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE_USER=os.environ.get('FLASK_DATABASE_USER'),
        DATABASE=os.environ.get('FLASK_DATABASE')
    )

#aqui podemos ver que importamos la carpeta de conexion a la base de datos
#  ademas invocamos la funcion que conecta la base de datos , pasandole como argumento nuestra app creada arriba
    from . import db
    db.init_app(app)

#Aqui importamos auth
#Para luego invocar nuestro blueprint ,es decir nuestra URL base la cual deberemos llamar para ejecutar nuestras plantillas
    from . import auth
    from . import todo
    app.register_blueprint(auth.bp)
    app.register_blueprint(todo.bp)



    @app.route('/hola')
    def hola():
        return 'Hola! Mundo!'

    return app