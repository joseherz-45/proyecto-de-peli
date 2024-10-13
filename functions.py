from datetime import datetime
from models import db, Movie


def guardar_peliculas(peliculas):
    """Función para guardar películas en la base de datos."""
    if not peliculas:
        print('No se recibieron películas para guardar.')  # Debug
        return

    for pelicula in peliculas:
        nueva_pelicula = Movie(
            title=pelicula['title'],
            overview=pelicula['overview'],
            release_date=pelicula['release_date'],
            poster_path=pelicula['poster_path']
        )
        print(f'Guardando película: {nueva_pelicula.title}')  # Debug
        db.session.add(nueva_pelicula)
    
    try:
        db.session.commit()
        print('Películas guardadas exitosamente.')  # Debug
    except Exception as e:
        db.session.rollback()  # Rollback en caso de error
        print(f'Error al guardar las películas: {str(e)}')  # Debug