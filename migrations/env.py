import logging
from logging.config import fileConfig

from flask import current_app
from alembic import context
from extensions import db  # Asegúrate de que esta línea esté correcta
# Configura el logging
fileConfig(context.config.config_file_name)
logger = logging.getLogger('alembic.env')

# Establece el metadata de los modelos
target_metadata = db.metadata
config = context.config


def get_engine_url():
    """Obtiene la URL de la base de datos desde la configuración de Flask."""
    return str(current_app.config.get('SQLALCHEMY_DATABASE_URI'))

def configure_context():
    """Configura el contexto de Alembic con la URL de la base de datos y metadata."""
    context.configure(
        url=get_engine_url(),
        target_metadata=target_metadata
    )

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    configure_context()
    url = context.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    configure_context()
    connectable = db.engine

    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('No changes in schema detected.')

    conf_args = current_app.extensions['migrate'].configure_args
    if conf_args.get("process_revision_directives") is None:
        conf_args["process_revision_directives"] = process_revision_directives

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            **conf_args
        )

        with context.begin_transaction():
            context.run_migrations()

# Ejecuta las migraciones en modo offline u online
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
