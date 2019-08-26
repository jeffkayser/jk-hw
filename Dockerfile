FROM python:3
ADD ./book /app
ADD ./requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
ENV FLASK_APP=book.app
ENV FLASK_ENV=development
EXPOSE 5000
CMD flask run --host=0.0.0.0
