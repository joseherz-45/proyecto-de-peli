# eliminar.py
from flask import session, flash, redirect, url_for
from models import db, Movie
import logging

# Configurar el logger
logging.basicConfig(level=logging.INFO)

def eliminar_peliculas(peliculas):
    try:
        if not isinstance(peliculas, list):
            logging.error('Se esperaba una lista de películas.')
            return False
        
        for pelicula in peliculas:
            # Asegúrate de que cada elemento de 'peliculas' contenga un 'id'
            if 'id' not in pelicula:
                logging.warning('Un diccionario de película no contiene un ID. Ignorando este elemento.')
                continue

            pelicula_existente = Movie.query.get(pelicula['id'])

            if pelicula_existente:
                db.session.delete(pelicula_existente)
                logging.info(f'Película con ID {pelicula["id"]} eliminada.')
            else:
                logging.info(f'La película con ID {pelicula["id"]} no se encontró.')

        db.session.commit()
        logging.info('Todas las películas eliminadas exitosamente.')
        flash('Películas eliminadas exitosamente.', 'success')  # Mensaje para el usuario
        return True  # Devuelve True si todo salió bien

    except Exception as e:
        db.session.rollback()
        logging.error(f'Error al eliminar películas: {e}')
        flash('Error al eliminar las películas. Inténtalo de nuevo.', 'danger')  # Mensaje de error para el usuario
        return False  # Devuelve False si hubo un error