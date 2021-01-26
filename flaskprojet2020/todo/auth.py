#Functools son una serie de funciones que nos ayudan a hacer buen codigo
import functools

#Blueprint nos permite controlar el inicio,registro y cierre de sesion
#flash nos permite mandar mensajes al momento quizas de obtener un error de coneccion
#g es una variable global que podemos usar en todo el codigo
#render_template nos permite renderizar o invocar plantillas de HTML o CSS
# request nos permite enviar y resivir avisos de HTTP
#url_for nos permite crear una URL
#sesion nos permite mantener el control sobre que usuario está revisando cada informacion dependiendo de su sesion
from flask import(
    Blueprint, flash, g, render_template, request, url_for, session, redirect
)

#werkzeug.security importamos la creacion de contraseñas encriptadas y luego la revision de esas contraseñas para permitir el inicio de sesion
from werkzeug.security import check_password_hash, generate_password_hash


#Aqui importamos la coneccion de la base de datos
from todo.db import get_db


#Aqui creamos nuestro bluepirnt o plano
# dentro le asignamos un nombre, luego le decimos donde estará alojado , en este caso en nuestra aplicacion FLASK
# luego en url_prefix colocamos el rul base para nuestra web , entonces la base seria HTTP//:localhost/auth/OTRO enlace a algo
bp = Blueprint('auth', __name__, url_prefix='/auth')



#Lo primero es crear una ruta en mi blueprint donde indicaremos el url y ademas los metodos HTTP que este tendrá
#Luego definimos una funcion, en este caso register
# lo primero es validar si es que el metodo de la request es POST(osea que manda hacia la WEB) , si es POST lo que hacemos es guardar en variables los request de los formularios 
#  que vamos a crear. Ademas inicializamos las variables db y c como get_db , ademas de indicar que error = es NONE
# Luego ejecutamos usando la variable c le consulta SQL para sacar el id del usuaio en la tabla 

#Luego validamos si se rellenaron el username y la password , si no es asi asignamos un valor a la variable error
# Ademas mediante c.fetchone validamos si en la consulta anterior nos devolvio un valor, si no es None significa que ese ID ya existia entonces daremos un valor al error
# Pero si error es None , eso quiere decir que podemos registrarlo , entonces procedemos a realizar la ejecucion de la sentencia SQL
#  dandole un commit() para gurdadr bien los datos y redirigiendolo a una URL que nosotros queramos 
# tambien cargamos el error en flash 
# Y finalmente un vez terminado todos las validaciones renderizamos una plantilla a gusto, en este caso register, ya que si no se cumplen las cosas anteriores que son POST
# entonces vuelve a cargar la pagina de registro.

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db, c = get_db()
        error = None
        c.execute(
            'SELECT id FROM user WHERE username = %s'
        )
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif c.fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (%s, %s)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')



#






@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db,c = get_db()
        error = None
        c.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        )
        user = c.fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user=None
    else:
        db,c = get_db()
        c.execute(
            'SELECT * from user where id = %s', (user_id,)
        )
        g.user = c.fetchone()


#Esto es una funcion decoradora , definimos view que representa un endpoint
#Lo que hace esto es preguntar si hay un usuario loggeado o no
#si no esttá lo redirigimos a login
# pero si está lo dejamos en la vista 
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view