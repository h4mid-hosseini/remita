FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev gettext \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y gcc \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/
RUN chmod +x /app/entrypoint.sh

ENV DJANGO_SETTINGS_MODULE=exchange_accounting.settings

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "exchange_accounting.wsgi:application", "-b", "0.0.0.0:8000", "--workers", "2", "--threads", "2", "--timeout", "60"]
