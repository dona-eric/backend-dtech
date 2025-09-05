FROM python:3.12-slim

## repertoire de travail
WORKDIR /app

# installer les dépendances essentielles
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

## copy le file requiements.txt
COPY requirements.txt /app/


# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le projet
COPY . .

# Variables d’environnement
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=backend.settings

COPY start.sh /app/start.sh

RUN chmod +x /app/start.sh
ENTRYPOINT [ "/app/start.sh" ]
# Exposer le port
EXPOSE 8000

# Commande par défaut
CMD ["gunicorn", "--bind", "127.0.0.1:8000", "--workers", "3", "backend.wsgi:application"]
