FROM python:3.9

WORKDIR /app

COPY pipfile .
COPY pipfile.lock .

RUN  pip install --trusted-host pypi.python.org pipenv 
RUN pipenv install

COPY . .

ENTRYPOINT ['python', 'spot.py']



