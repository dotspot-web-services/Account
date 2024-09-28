# for the sake of docker compose

FROM python:3.12-alpine AS build

ENV PYROOT /pyroot
ENV PYTHONUSERBASE $PYROOT

FROM build AS builder

RUN apk update && \
    apk add --upgrade && apk add openldap-dev build-base linux-headers \
    musl-dev fuse fuse-dev libffi-dev
RUN pip install --upgrade pip && pip install pipenv --no-cache-dir
#WORKDIR /app

COPY Pipfile* .

RUN PIP_USER=1 PIP_IGNORE_INSTALLED=1 pipenv install --system --deploy --ignore-pipfile

##cmd:pip3# Final stage
FROM build

#WORKDIR /app

#RUN set -ex \
#    # Create a non-root user
#    && addgroup --system --gid 1001 appgroup \
#    && adduser --system --uid 1001 --gid 1001 --no-create-home appuser \
#    # Upgrade the package index and install security upgrades
#    && apt-get update \
#    && apt-get upgrade -y

COPY --from=builder $PYROOT/lib/ $PYROOT/lib/
COPY --from=builder $PYROOT/bin/ $PYROOT/bin/

ENV PATH="$PYROOT/bin:$PATH"

# Create and switch to a new user
RUN addgroup -S accgroup && adduser -S accuser -G accgroup

# Tell docker that all future commands should run as the appuser user
WORKDIR /home/accapp
USER accuser
COPY ./src .
COPY README.md .

# Clean up
#RUN apt-get autoremove -y \
#    && apt-get clean -y \
#    && rm -rf /var/lib/apt/lists/*

EXPOSE 8000
#CMD [ "uwsgi", "--socket", "0.0.0.0:3031", \
#               "--uid", "uwsgi", \
#               "--protocol", "uwsgi", \
#               "--wsgi", "wsgi:account" ]
#
CMD ["uwsgi", "--ini", "wsgi.ini"]

#CMD ["--ini", "src/setapp/wsgi.py"]

# Set the user to run the application
COPY --chown=app:app . /accapp
