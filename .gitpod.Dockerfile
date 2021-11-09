FROM gitpod/workspace-full
                
USER root
RUN sudo apt-get update
RUN sudo apt-get upgrade
RUN sudo apt install python-is-python3
RUN python3 -m pip install --upgrade pip
RUN alias python=python3