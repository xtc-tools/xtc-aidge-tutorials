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
COPY .binder/aidge_requirements.txt /docker/aidge_requirements.txt
COPY .binder/entrypoint.sh /docker/entrypoint.sh
RUN chmod +x /docker/entrypoint.sh

# Install requirements
RUN pip install --no-cache-dir -r /docker/requirements.txt

# Install Aidge modules
RUN pip install --no-cache-dir -r /docker/aidge_requirements.txt

# Install XTC
ENV XTC_REPO=https://github.com/guillon/xtc
ENV XTC_REVISION=e9ece26f56271b1f819e8d96352f704356781f51
RUN git clone $XTC_REPO /root/xtc && \
    cd /root/xtc && \
    git checkout $XTC_REVISION && \
    pip install --no-cache-dir . && \
    pip install --no-cache-dir -r tvm_requirements.txt && \
    pip install --no-cache-dir -r mlir_requirements.txt

# Install Aidge Export Compile
ENV AEC_REPO=https://gitlab.eclipse.org/cguillon/aidge-export-compile
ENV AEC_REVISION=a8a45f96ac3423b9f4fd3c836b6cccd65f824f9a
RUN git clone $AEC_REPO /root/aidge-export-compile && \
    cd /root/aidge-export-compile && \
    git checkout $AEC_REVISION && \
    pip install --no-cache-dir .

# Install Aidge Benchmarks
ENV AB_REPO=https://gitlab.eclipse.org/cguillon/aidge_benchmark
ENV AB_REVISION=b2c357fc92c4cf2b136553da05954481c2d2e797
RUN git clone $AB_REPO /root/aidge_benchmark && \
    cd /root/aidge_benchmark && \
    git checkout $AB_REVISION && \
    pip install --no-cache-dir .

# Patch aidge
COPY .binder/aidge_core.patch /docker/
COPY .binder/aidge_export_cpp.patch /docker
RUN cd /usr/local/lib/python3.10/site-packages/ && patch -p1 -i /docker/aidge_core.patch || true
RUN cd /usr/local/lib/python3.10/site-packages/ && patch -p1 -i /docker/aidge_export_cpp.patch || true

# # Patch server.py from ai_edge_model_explorer to run on Binder
# COPY .binder/patched_server.py /tmp/patched_server.py
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
