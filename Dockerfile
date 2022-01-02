# init a base image (Alpine is small Linux distro)

FROM alpine:latest

# This hack is widely applied to avoid python printing issues in docker containers.
# See: https://github.com/Docker-Hub-frolvlad/docker-alpine-python3/pull/13
#ENV PYTHONUNBUFFERED=1



RUN apk update && apk add python3-dev \
                        gcc \
                        libc-dev
#RUN apk add --no-cache python3-dev

WORKDIR /app

COPY . /app

RUN pip -r requirements.txt

EXPOSE 5000

ENTRYPOINT  ["python3"]

CMD ["app.py"]



