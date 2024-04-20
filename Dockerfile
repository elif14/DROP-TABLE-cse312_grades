FROM python:3.12
ENV HOME /root
WORKDIR /root

COPY . .

RUN pip3 install -r requirements.txt

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

RUN python3 -m pip install gevent

RUN pip3 install gunicorn

CMD /wait && gunicorn -k gevent -b 0.0.0.0:8080 server:app