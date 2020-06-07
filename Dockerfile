FROM python:3.8-slim-buster
COPY logspout-tme.py /opt/
COPY requirements.txt /opt/
COPY secret /opt/secret
WORKDIR /opt
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN pip install -r requirements.txt
CMD ["python", "-u", "logspout-tme.py"]
