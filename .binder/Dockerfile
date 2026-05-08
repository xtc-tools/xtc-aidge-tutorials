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
COPY .binder/Dockerfile /docker/Dockerfile
COPY .binder/requirements.txt /docker/requirements.txt
COPY .binder/entrypoint.sh /docker/entrypoint.sh
RUN chmod +x /docker/entrypoint.sh

# Install requirements
RUN pip install --no-cache-dir -r /docker/requirements.txt

# # Install Aidge modules
# RUN pip install --upgrade --no-cache-dir \
#     aidge-core \
#     aidge-backend-cpu \
#     aidge-learning \
#     aidge-export-cpp \
#     aidge-onnx \
#     aidge-quantization \
#     aidge-backend-cuda \
#     aidge-backend-opencv \
#     aidge-model-explorer \
#     aidge-export-arm-cortexm

# # Patch server.py from ai_edge_model_explorer to run on Binder
# COPY ./.binder/patched_server.py /tmp/patched_server.py
# RUN python -c "import model_explorer, os; import shutil; shutil.copy('/tmp/patched_server.py', os.path.join(os.path.dirname(model_explorer.__file__), 'server.py'))"

# Copy tutorials files to writable directory
RUN mkdir -p ${HOME}/work
COPY ./tutorials ${HOME}/work
RUN chown -R ${NB_USER}:${NB_USER} ${HOME}/work

# Create writable dir for 
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
