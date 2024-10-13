from flask import render_template, request, redirect, url_for, flash
from models import db, Movie

def actualizar_pelicula_get(id):
    pelicula = Movie.query.get(id)
    if pelicula:
        return render_template('actualizar_pelicula.html', pelicula=pelicula)
    else:
        flash('Película no encontrada.', 'danger')
        return redirect(url_for('carrito'))

def actualizar_pelicula_post(id):
    pelicula = Movie.query.get(id)
    if pelicula:
        pelicula.title = request.form['title']
        pelicula.overview = request.form['overview']
        pelicula.release_date = datetime.strptime(request.form['release_date'], '%Y-%m-%d').date()
        pelicula.poster_path = request.form['poster_path']
        db.session.commit()
        flash('La película ha sido actualizada correctamente.', 'success')
    else:
        flash('Película no encontrada.', 'danger')
    return redirect(url_for('carrito'))
