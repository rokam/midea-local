FROM mcr.microsoft.com/devcontainers/python:1-3.11

# [Option] Install Node.js
ARG INSTALL_NODE="true"
ARG NODE_VERSION="lts/*"
RUN if [ "${INSTALL_NODE}" = "true" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

# Install Python dependencies from requirements
COPY requirements*.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements-all.txt \
   && rm -rf /tmp/pip-tmp

RUN pip3 --disable-pip-version-check --no-cache-dir install pre-commit

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

# Set the default shell to bash instead of sh
ENV SHELL /bin/bash
