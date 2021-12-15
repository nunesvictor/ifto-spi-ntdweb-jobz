FROM python:3.9.7-slim

RUN groupadd -g 1000 guest && \
    useradd -u 1000 -g 1000 -m guest

USER guest

ENV PYTHONUNBUFFERED=1
ENV HOME="/home/guest"
ENV PATH="$HOME/.local/bin:$PATH"

ARG APP_NAME="jobz"
ARG APP_HOME="$HOME/${APP_NAME}/"

RUN mkdir -p ${APP_HOME}
WORKDIR ${APP_HOME}

COPY pyproject.toml pdm.lock ${APP_HOME}

RUN pip install -U pip && \
    pip install --user pdm && \
    pdm install --dev

RUN pdm --pep582 bash >> $HOME/.bashrc

COPY entrypoint.sh ${APP_HOME}

COPY --chown=1000:1000 src ${APP_HOME}/src/

CMD ["./entrypoint.sh"]
