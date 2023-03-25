FROM python:slim-bullseye

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
    make \
    curl \
    openssh-server

# Start ssh client.
RUN service ssh start

# Configure sudo for initialization tasks. 
RUN echo "NRuser ALL=(ALL) NOPASSWD: /home/NRuser/flaskapp/scripts/init.sh" >> /etc/sudoers && \
    echo "NRuser ALL=(ALL) NOPASSWD: /bin/chown" >> etc/sudoers

# D2 installation.
RUN curl -fsSL https://d2lang.com/install.sh | sh -s --

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

# # Copy cli shortcuts for permanent use.
# RUN cp ${workdir}/scripts/shortcuts.sh ${reldir}/.bashrc


