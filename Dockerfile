FROM python:3.8

ENV DOCKER_HOST=0.0.0.0

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]