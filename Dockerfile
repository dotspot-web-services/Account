# for the sake of docker compose

FROM python:3.12-slim as build

ENV PYROOT /pyroot
ENV PYTHONUSERBASE $PYROOT

RUN apt-get update && \
    apt-get upgrade && \
    apt-get install -y --no-install-recommends libldap2-dev libsasl2-dev libssl-dev && \
    apt-get clean autoclean && rm -rf /var/lib/apt/* /var/cache/apt/* && \
    apt-get autoremove --purge && \
    pip install pipenv --no-cache-dir

WORKDIR /app

COPY Pipfile* .

RUN PIP_USER=1 PIP_IGNORE_INSTALLED=1 pipenv install --system --deploy --ignore-pipfile

### Final stage
FROM python:3.12-slim as final

WORKDIR /app

RUN set -ex \
    # Create a non-root user
    && addgroup --system --gid 1001 appgroup \
    && adduser --system --uid 1001 --gid 1001 --no-create-home appuser \
    # Upgrade the package index and install security upgrades
    && apt-get update \
    && apt-get upgrade -y

COPY --from=build $PYROOT/lib/ $PYROOT/lib/
COPY ./src src


# Clean up
RUN apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8000

ENTRYPOINT [cmd, "--ini", "src/setapp/wsgi.py"]

# Set the user to run the application
COPY --chown=app:app . /app
