from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from models import db, Movie
import requests
from sqlalchemy.exc import IntegrityError
import os
from datetime import datetime
from flask_cors import CORS
from werkzeug.utils import secure_filename

# Inicializar la aplicación Flask
app = Flask(__name__)

# Configuración de la base de datos SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mi_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.secret_key = os.getenv('SECRET_KEY', 'tu_clave_secreta_aqui')

# Inicializar la base de datos y CORS
db.init_app(app)
CORS(app)

# API de la aplicación
API_KEY = '8e6a62b2451f8dac3892516721ac9a1e'

# Crear la base de datos
with app.app_context():
    db.create_all()



def obtener_peliculas_populares():
    """Obtener películas populares desde TMDB."""
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&language=en-US&sort_by=popularity.desc&page=1"
    response = requests.get(url)

    if response.status_code == 200:
        try:
            resultados = response.json().get('results', [])
            return [
                {
                    'title': pelicula['title'],
                    'overview': pelicula['overview'],
                    'release_date': pelicula['release_date'],
                    'poster_path': pelicula['poster_path'],
                }
                for pelicula in resultados
            ]
        except ValueError:
            print("La respuesta no es un JSON válido")
            return []
    else:
        print(f"Error en la solicitud: {response.status_code}")
        return []


   #"esta es de mi base de datos"
@app.route('/')
def home():
    """Página principal que muestra las películas guardadas y populares."""
    movies = Movie.query.all()  # Manteniendo la consulta para obtener las películas guardadas
    peliculas_populares = []  # Esta lista puede quedarse vacía si no se usan datos externos

    # Si no hay películas guardadas, puedes optar por no hacer nada o mostrar un mensaje
    if not movies:
        # Aquí podrías obtener películas populares si lo deseas, pero no es necesario
        # peliculas_populares = obtener_peliculas_populares()
        pass  # No hacemos nada si no hay películas

    return render_template('index.html', movies=movies, peliculas_populares=peliculas_populares)

#Esta es mi base de datos y la Apis Rest
#@app.route('/')
#def home():
    """Página principal que muestra las películas guardadas y populares."""
    # movies = Movie.query.all()  # Comentado para desconectar la API de la base de datos
    #peliculas_populares = []

    # if not movies:  # Comentado para evitar la lógica de base de datos
    #     peliculas_populares = obtener_peliculas_populares()
    #     for pelicula in peliculas_populares:
    #         if not Movie.query.filter_by(title=pelicula['title']).first():
    #             nueva_pelicula = Movie(
    #                 title=pelicula['title'],
    #                 overview=pelicula['overview'],
    #                 release_date=datetime.strptime(pelicula['release_date'], '%Y-%m-%d') if pelicula['release_date'] else None,
    #                 poster_path=pelicula['poster_path']
    #             )
    #             db.session.add(nueva_pelicula)
    #     db.session.commit()

    #return render_template('index.html', movies=movies, peliculas_populares=peliculas_populares)







def allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/editar_pelicula/<int:movie_id>', methods=['POST'])
def editar_pelicula(movie_id):
    movie = db.session.get(Movie, movie_id)
    if not movie:
        return jsonify({"mensaje": "Película no encontrada."}), 404
    
    title = request.form.get('title')
    overview = request.form.get('overview')
    release_date_str = request.form.get('release_date')

    if not title or not overview or not release_date_str:
        return jsonify({"mensaje": "Todos los campos son obligatorios."}), 400

    try:
        release_date = datetime.strptime(release_date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"mensaje": "Fecha de lanzamiento no válida."}), 400

    movie.title = title
    movie.overview = overview
    movie.release_date = release_date

    if 'image_file' in request.files:
        file = request.files['image_file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)  # Asegúrate de que esto no tenga barras
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])

            try:
                file.save(file_path)
                movie.poster_path = filename  # Solo el nombre del archivo
            except Exception as e:
                return jsonify({"mensaje": "Error al guardar el archivo.", "error": str(e)}), 500

    try:
        db.session.commit()
        return jsonify({"mensaje": "Película editada exitosamente."}), 200
    except Exception as e:
        db.session.rollback()
        print(f'Error al editar la película: {e}')  # Para depuración
        return jsonify({"mensaje": "Error al editar la película.", "error": str(e)}), 500

def allowed_file(filename):
    # Define las extensiones permitidas para las imágenes
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


@app.route('/eliminar_pelicula/<int:movie_id>', methods=['DELETE'])
def eliminar_pelicula(movie_id):
    movie = db.session.get(Movie, movie_id)
    if not movie:
        return jsonify({"mensaje": "Película no encontrada."}), 404

    try:
        db.session.delete(movie)
        db.session.commit()
        return jsonify({"mensaje": "Película eliminada con éxito."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"mensaje": "Error al eliminar la película.", "error": str(e)}), 500
    
    
 
   
@app.route('/agregar_pelicula', methods=['POST'])
def agregar_pelicula():
    title = request.form.get('title')
    overview = request.form.get('overview')
    release_date = request.form.get('release_date')
    image_file = request.files.get('image_file')

    if not title or not overview or not release_date:
        return jsonify({'mensaje': 'Todos los campos son obligatorios.'}), 400

    # Manejo de la imagen
    if image_file:
        filename = secure_filename(image_file.filename)
        image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    else:
        filename = 'default_poster.jpg'  # Imagen por defecto

    new_movie = Movie(
        title=title,
        overview=overview,
        release_date=release_date,
        poster_path=filename
    )

    try:
        db.session.add(new_movie)
        db.session.commit()
        return jsonify({'mensaje': 'Película agregada exitosamente'}), 201
    except Exception as e:
        db.session.rollback()
        print(f'Error al agregar la película: {e}')  # Para depuración
        return jsonify({'mensaje': 'Error al agregar la película.', 'error': str(e)}), 500





if __name__ == '__main__':
    app.run(debug=True)
