FROM python:3.6-slim

WORKDIR /app

RUN apt-get clean && apt-get -y update
RUN apt-get -y install nginx
RUN apt-get -y install vim
RUN apt-get -y install python3-dev
RUN apt-get -y install git

# RUN apt-get -y install build-essential
# RUN apt-get -y install python-certbot-nginx

COPY ../requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt

COPY start.sh /app/deployment/start.sh
RUN chmod +x /app/deployment/start.sh
CMD ["nginx", "-g", "daemon off;"]