FROM python:3.12.0a6-slim-bullseye

# use bash shell.
ENV SHELL=/bin/bash

# define user variables for account setup.
ARG username=NRuser
ARG reldir=/home/${username}
ARG workdir=${reldir}/airkeys

RUN apt-get update && \
    apt-get --no-install-recommends -y install git \
    dos2unix \
    bash-completion \
    sudo \
    vim \
    openssh-server

# Start ssh client.
RUN service ssh start

# Configure sudo for initialization tasks. 
RUN echo "NRuser ALL=(ALL) NOPASSWD: /home/NRuser/flaskapp/scripts/init.sh" >> /etc/sudoers && \
    echo "NRuser ALL=(ALL) NOPASSWD: /bin/chown" >> etc/sudoers

# Create and switch to non-Root User.
RUN useradd --home-dir ${reldir} ${username}

USER ${username}
WORKDIR ${workdir}

# Create virtaul env.
RUN python3 -m venv ${reldir}/env
ENV PATH=${reldir}/env/bin:$PATH

# Update Package Management
RUN pip install --upgrade pip

# Copy source files
COPY . .

# Copy cli shortcuts for permanent use.
RUN cp ${workdir}/scripts/shortcuts.sh ${reldir}/.bashrc


