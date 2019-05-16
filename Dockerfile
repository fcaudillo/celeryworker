FROM python:3

WORKDIR /usr/src/app

ADD requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
ENV QUEUE_RELOAD celery_dummy
ADD recargasyservicios.py tasks.py celeryconfig.py ./
RUN rm -f /etc/localtime
RUN ln  -s  /usr/share/zoneinfo/America/Mexico_City /etc/localtime

CMD celery -A tasks worker --loglevel=info -Q $QUEUE_RELOAD