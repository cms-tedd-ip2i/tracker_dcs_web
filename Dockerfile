FROM python:3.9

RUN apt-get update && apt-get -y upgrade

WORKDIR /app

# install dependencies

COPY requirements ./requirements
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements/docker.txt

# install this package

COPY tracker_dcs_web/ ./tracker_dcs_web
COPY setup.py ./
RUN pip install -e .

# prepare storage dir
RUN mkdir -p /app/files
ENV STORAGE_DIR=/app/files

# create user
RUN useradd appuser
RUN chown -R appuser /app/files

USER appuser

