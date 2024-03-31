FROM gitpod/workspace-full

USER gitpod

# Copy the .python-version file into the Docker image to use it during the build
COPY .python-version /home/gitpod/.python-version

# Install the specific Python version from .python-version and upgrade pip
RUN pyenv install $(cat /home/gitpod/.python-version) && \
    pyenv global $(cat /home/gitpod/.python-version) && \
    eval "$(pyenv init -)" && \
    pip install --upgrade pip