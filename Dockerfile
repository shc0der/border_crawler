FROM python:3.8.12-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV APP_HOME=/home
ENV PYTHONPATH "${PYTHONPATH}:$APP_HOME"

ENV VIRTUAL_ENV=${APP_HOME}/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR $APP_HOME

COPY ./requirements.txt ./
COPY ./docker-entrypoint.sh ./

RUN chmod +x ./docker-entrypoint.sh

COPY ./app ${APP_HOME}/app
COPY ./.env ${APP_HOME}/.env
COPY ./alembic.ini ${APP_HOME}/alembic.ini

RUN pip install --no-cache-dir --upgrade pip &&\
    pip install -r requirements.txt &&\
    rm -rf /root/.cache/pip &&\
    rm requirements.txt

ENTRYPOINT ["./docker-entrypoint.sh"]