FROM tensorflow/tensorflow:latest-py3

# Установка необходимых пакетов
RUN apt-get update
RUN apt-get install -y  libsm6 libxrender1 libxext-dev 
RUN pip install opencv-python

# Нужно чтобы не было проблем с кодировкой
RUN export PYTHONIOENCODING=utf-8

# Копируем наш код в notebooks
COPY . /notebooks

LABEL maintainer="lenok-cotik@yandex.ru"