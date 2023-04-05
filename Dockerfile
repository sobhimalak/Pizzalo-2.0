FROM python:3.8



WORKDIR /usr/src/app

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

RUN pip install -r requirements.txt

EXPOSE 5000

CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]