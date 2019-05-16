FROM python:3

WORKDIR /usr/src/app

ADD requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
ENV QUEUE_RELOAD celery_dummy
ADD recargasyservicios.py tasks.py celeryconfig.py ./
RUN rm -f /etc/localtime
RUN ln  -s  /usr/share/zoneinfo/America/Mexico_City /etc/localtime
ARG BUILD_USU_MQ
ARG BUILD_PASS_MQ

ENV USUARIO_MQ=$BUILD_USU_MQ
ENV PASSWORD_MQ=$BUILD_PASS_MQ

CMD celery -A tasks worker --loglevel=info -Q $QUEUE_RELOAD