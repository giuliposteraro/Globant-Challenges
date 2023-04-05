FROM python:3.10
EXPOSE 5000
WORKDIR /app
RUN pip install flask
RUN pip install flask_restful
RUN pip install flask_sqlalchemy
RUN pip install flask_migrate
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]
