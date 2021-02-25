FROM python:3.9.1-alpine3.12 as base

MAINTAINER Matei Marica

#RUN apk update -y && \
#    apk install -y python3-pip python3.6

# Copy the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

EXPOSE 5000

COPY ./src /app/

#ENTRYPOINT ["python3.6"]

CMD ["python" ,"app.py"]
