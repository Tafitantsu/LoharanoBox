# ==========================
# STAGE 1 : Builder
# ==========================
FROM python:3.12-slim-bookworm AS builder

WORKDIR /app

# Installer dépendances système minimales pour pip build
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        libffi-dev \
        libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier requirements
COPY requirements.txt .

# Créer venv et installer dépendances Python
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip setuptools wheel \
    && /opt/venv/bin/pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu \
    && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt \
    && find /opt/venv -name "*.pyc" -delete \
    && find /opt/venv -type d -name "tests" -exec rm -rf {} +

# ==========================
# STAGE 2 : Runtime léger
# ==========================
FROM python:3.12-slim-bookworm

# Copier le venv optimisé depuis le builder
COPY --from=builder /opt/venv /opt/venv

# Activer venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Copier le code source
COPY . .

# Exposer le port
EXPOSE 8000

# Démarrage
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
