FROM python:3-onbuild
RUN pip3 install -r requirements.txt
WORKDIR    /app
COPY . /usr/src/app
CMD ["python", "cliente.py"]
