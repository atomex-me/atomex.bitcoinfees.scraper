FROM python:3.10-alpine
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ .
CMD [ "/bin/sh", "./run.sh" ]