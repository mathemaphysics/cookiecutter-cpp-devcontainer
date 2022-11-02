FROM {{cookiecutter.container_image}}

ARG DEVUSER devuser

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update \
 && apt-get -y install --no-install-recommends build-essential \
 					       g++ \
					       gdb \
						   doxygen \
					       git \
					       openssh-client \
						   openssl \
						   libssl-dev \
					       wget \
					       vim \
					       sudo \
					       libboost-all-dev \
					       libopencv-dev \
					       python3 \
					       python3-dev \
					       python3-pip \
					       python3-numpy \
 && python3 -m pip install cookiecutter sphinx breathe sphinx_rtd_theme
{%- if cookiecutter.cmake_build_version != "None" %}
WORKDIR /builds
RUN git clone https://github.com/Kitware/CMake.git -b v{{cookiecutter.cmake_build_version}} \
 && cd CMake && ./configure --prefix=/usr && make && make install
{%- endif %}

ENV DEVUSER=${DEVUSER}
RUN adduser --uid 1000 --disabled-password --gecos "" ${DEVUSER} \
    && echo "${DEVUSER} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${DEVUSER} {% if cookiecutter.docker_in_docker == "Yes" %}\{%- endif %}
{%- if cookiecutter.docker_in_docker == "Yes" %}
    && groupadd docker && usermod -aG docker ${DEVUSER} && newgrp docker

RUN apt-get -y update \
    && apt-get -y install openssh-client openssl libssl-dev wget vim \
    && apt-get -y install ca-certificates curl gnupg lsb-release acl \
    && apt-get -y remove docker docker.io containerd runc \
    && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null \
    && apt-get -y update \
    && apt-get -y install docker-ce-cli docker-compose-plugin
{%- endif %}

USER ${DEVUSER}

{%- if cookiecutter.docker_in_docker == "Yes" %}
CMD sudo setfacl -m "g:docker:rw" /var/run/docker.sock
RUN echo >>/home/${DEVUSER}/.profile && echo "sudo setfacl -m \"g:docker:rw\" /var/run/docker.sock" >>/home/${DEVUSER}/.profile
{%- endif %}

