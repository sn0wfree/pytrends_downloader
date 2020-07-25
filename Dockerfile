FROM python:3.7

COPY ./ /tmp/
WORKDIR /tmp/
RUN  pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

EXPOSE 5672
CMD python run.py



