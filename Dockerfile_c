FROM ubuntu:latest
RUN apt update && DEBIAN_FRONTEND=noninteractive apt install -y gcc make git binutils libc6-dev gdb sudo
RUN adduser --disabled-password --gecos '' user
RUN echo 'user ALL=(root) NOPASSWD:ALL' > /etc/sudoers.d/user
RUN apt-get install -y gnuplot 
USER user
WORKDIR /home/user