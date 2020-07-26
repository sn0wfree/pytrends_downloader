FROM amancevice/pandas:alpine

COPY ./ /tmp/
WORKDIR /tmp/
RUN apk add musl-dev gcc make libxml2-dev libxslt-dev && \
    pip install --no-cache-dir -r requirements.txt 

EXPOSE 5672
CMD python server.py
