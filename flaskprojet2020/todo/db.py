import mysql.connector
#click nos va a servir para ejecutar comandos en la terminal
import click
#current_app nos sire para mantener la app que estamos ejecutando, g es una variable global , que le podemos dar un valor y luego llamarlo de cualquier lugar
from flask import current_app, g
#appcontext nos sirve para acceder a variables escritas como el HOST,PASSWORD o la BD
from flask.cli import with_appcontext
#este es el enlace con la coneccion con la sintaxis de mysql
from .schema import instructions


#Aqui vemos como se crea una coneccion a la base de dato, retornando dentro de la variable g tanto la coneccion de BD y el cursor 
#al comienzo del if preguntamos db está en g , si no está entonces conectate  ademas crea el cursor y lo guarda en g

def get_db():
    if 'db' not in g:
        g.db= mysql.connector.connect(
            host=current_app.config['DATABASE_HOST'],
            user=current_app.config['DATABASE_USER'],
            password=current_app.config['DATABASE_PASSWORD'],
            database=current_app.config['DATABASE'],
        )
        g.c = g.db.cursor(dictionary=True)
    return g.db, g.c


#aqui creamos la desconeccion a la base de datos 
#la variable db la inicializamos en None , con g.pop podemos eliminar el primer argumento que le pasemos. entonces de esa manera estariamos eliminando el argumento db de g 
# lo convertiriamos en None

#luego en el if preguntamos si db no es None , entonces cierra la coneccion de la db

def close_db(e=None):
    db = g.pop('db',None)

    if db is not None:
        db.close()


#Aqui definimos la funcion que va a leer las intrucciones SQL y luego las va a ejecutar
#Podemos ver como las iteramos en i y las ejecutamos 
#definimos tanto db, c = con la funcion para establecer coneccion
#finalmente hacemos un commit(), fuera del if para guardar todas las instrucciones iteradas

def init_db():
    db, c = get_db()
    for i in instructions:
        c.execute(i)

    db.commit()


#Aqui podemos ver la funcion que ejecuta un comando en la terminal y luego nos da un mensaje a nosotros que nos permite saber si se realizo la coneccion con exito o no
# lo que hace es init_db , osea lee las instrucciones  y las ejecuta 
# y finalmente mediante la funcion click.echo no da un mensaje an la terminal de la web

#para que todo esto funcione debemos invocar estas funciones de abajo
#click.command que es para que podamos manualmente en la terminal preguntar si el Script se ejecuto con exito , mediante el comando , flask init-db
#con with.appcontext lo que hacemos es permitir que utilice el contexto de la aplicacion, osea que le damos permiso para que pueda obtener DATA_BASE HOST,PASSWORD,USER,DATABASE 

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Base de Datos Inicializada')











#Esta funcion lo que hace es 
# llamamos a nuestra app de flask , y la funcion teardown_appcontext hace referencia a cuando se esta terminando la ejecucion de el argumento que le pasemos
# en este caso app, entonces cuando este terminando de ejecutarse app , hará lo que nosotros le hallamos pasado en teardown_appcontext(), en este caso ejecutaria la funcion close_db
# en otras palabras, una vez esté finalizando la ejecucion de app , se ejecutara close_db , cerrando la conexion a la BD
#Finalmente añadimos la funcion de init_db_command para poder ejecutar la coneccion a la BD

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)