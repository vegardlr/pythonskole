FROM gitpod/workspace-full-vnc
RUN pip install matplotlib
RUN pip install ephem
RUN sudo apt-get install -y python3-tk

