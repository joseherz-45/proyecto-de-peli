import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Configuración de la base de datos
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'mi_app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False