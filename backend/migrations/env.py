# migrations/env.py

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import sys
import os

# Ajout du chemin de l'app pour les imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.db.base import Base  # Base avec tous les modèles importés
from app.core.config import settings

# Configuration Alembic
config = context.config

# Chargement des loggers de alembic.ini
fileConfig(config.config_file_name)

# Définition des métadonnées pour la génération automatique
target_metadata = Base.metadata

# URL de connexion depuis .env (via config.py)
def get_url():
    return settings.DATABASE_URI

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        {
            "sqlalchemy.url": get_url()
        },
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

# Point d'entrée
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
