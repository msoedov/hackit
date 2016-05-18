FROM python:3.5

WORKDIR /app
ENV FILES_VOLUME /files
EXPOSE 7001
COPY ./requirements.txt .
RUN pip install -r requirements.txt ipdb==0.9.3 --no-cache-dir --disable-pip-version-check
VOLUME /files
COPY ./app .
