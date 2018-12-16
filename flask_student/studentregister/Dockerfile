# MAINTAINER        FWJ <a364580936@gmail.com>
# DOCKER-VERSION    18.06.1-ce

FROM python:3.6.5
LABEL maintainer="a364580936@gmail.com"
COPY pip.conf /root/.pip/pip.conf

RUN mkdir -p /usr/src/app && \
    mkdir -p /var/log/gunicorn

WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/requirements.txt


RUN pip install --no-cache-dir gunicorn && \
    pip install --no-cache-dir -r /usr/src/app/requirements.txt

COPY . /usr/src/app

EXPOSE  5000

CMD ["/usr/local/bin/gunicorn", "-w", "2", "-b", ":5000", "manage:app"]