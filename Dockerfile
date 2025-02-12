FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt



COPY ./app /code/app
COPY ./prisma /code/prisma

RUN mkdir -p /code/.cache/prisma-python/binaries && chmod -R 777 /code/.cache
ENV PRISMA_CACHE_DIR="/code/.cache/prisma-python"


RUN prisma generate
#RUN prisma migrate deploy

# This can be overridden in .env if declared in docker-compose
ENV MODE=production

# Set MODE=development in .env when run locally to listen for changes
CMD ["sh", "-c", "if [ \"$MODE\" = 'development' ]; then fastapi dev app/main.py --host 0.0.0.0 --port 8080 --reload; else prisma migrate deploy && fastapi run app/main.py --host 0.0.0.0 --port 8080; fi"]

#CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8080"]
