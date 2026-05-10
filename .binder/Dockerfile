FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    wget \
    build-essential \
    libfmt-dev \
    tree \
    make \
    locales \
    time \
    git-core \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set up locales
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

ENV LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8

# Set up user
ARG NB_USER=jovyan
ARG NB_UID=1000
ENV USER=${NB_USER}
ENV HOME=/home/${NB_USER}

RUN useradd -m -s /bin/bash --uid ${NB_UID} ${NB_USER}

# Upgrade pip
RUN python -m pip install --upgrade pip

# Copy docker files
COPY .binder/requirements.txt /docker/requirements.txt
COPY .binder/requirements.txt /docker/aidge_requirements.txt
COPY .binder/entrypoint.sh /docker/entrypoint.sh
RUN chmod +x /docker/entrypoint.sh

# Install requirements
RUN pip install --no-cache-dir -r /docker/requirements.txt

# Install Aidge modules
RUN pip install --no-cache-dir -r /docker/aidge_requirements.txt

# Install XTC
ENV XTC_REPO=https://github.com/xtc-tools/xtc
ENV XTC_REVISION=f8246794a6951eb5627959e8d8e07f9ae9f6f070
RUN git clone $XTC_REPO /tmp/xtc && \
    cd /tmp/xtc && \
    git checkout $XTC_REV && \
    pip install --no-cache-dir . && \
    pip install --no-cache-dir -r mlir_requirements.txt && \
    pip install --no-cache-dir -r tvm_requirements.txt && \
    cd / && \
    rm -rf /tmp/xtc
      
# # Patch server.py from ai_edge_model_explorer to run on Binder
# COPY $BINDER_DIR/patched_server.py /tmp/patched_server.py
# RUN python -c "import model_explorer, os; import shutil; shutil.copy('/tmp/patched_server.py', os.path.join(os.path.dirname(model_explorer.__file__), 'server.py'))"

# Copy tutorials files to writable directory
RUN mkdir -p ${HOME}/work
COPY ./tutorials ${HOME}/work
RUN chown -R ${NB_USER}:${NB_USER} ${HOME}/work

# Create writable dir for matplotlib tmp
RUN mkdir -p /tmp/matplotlib && chown -R ${NB_USER} /tmp/matplotlib

# Switch to the working directory
WORKDIR  ${HOME}/work

# Switch to user
USER ${NB_USER}

# Set MPLCONFIGDIR 
ENV MPLCONFIGDIR=/tmp/matplotlib

# Set default command
ENTRYPOINT ["/docker/entrypoint.sh"]
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--allow-root"]
