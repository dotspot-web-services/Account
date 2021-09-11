
# Use base Python image from Docker Hub
FROM python:3.9


WORKDIR /app

COPY . .

# Set the working directory to /app
WORKDIR /app

# copy the requirements file used for dependencies
#COPY requirements.txt .
RUN pip install --upgrade pip

# Install any needed packages specified in requirements.txt
#RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN pip3 install --trusted-host pypi.python.org pipenv 

# Copy the rest of the working directory contents into the container at /app
COPY . .

RUN pipenv install --system --deploy --ignore-pipfile

# Run app.py when the container launches
ENTRYPOINT ["python", "src/accounts.py"]