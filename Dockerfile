FROM python:3.10-slim

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get -y install git && \
    rm -rf /var/lib/apt/lists/*



ARG FROM_PATH=.
ARG USER=service-user
ARG HOME=/home/$USER
ARG TO_PATH=$HOME/service
ARG VIRTUAL_ENV=$TO_PATH/venv

# Create service user
RUN /usr/sbin/useradd -m -u 5000 $USER
USER $USER

# Create service directory
RUN mkdir -p $TO_PATH
WORKDIR $TO_PATH

# Create virtual environment
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install --upgrade pip

# Copy necessary files
COPY $FROM_PATH/pyproject.toml pyproject.toml
COPY $FROM_PATH/.git .git

RUN mkdir ./tracker_dcs_web
RUN --mount=type=cache,target=$HOME/.cache/pip pip install .

# Copy service source code
COPY $FROM_PATH/tracker_dcs_web $TO_PATH/tracker_dcs_web

# prepare storage dir
RUN mkdir -p ${TO_PATH}/files
ENV STORAGE_DIR=/${TO_PATH}/files

ENV PYTHONPATH="$PWD:$PYTHONPATH"


