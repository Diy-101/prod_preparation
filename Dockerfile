FROM python:3.12.1-alpine3.19

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENV SERVER_PORT=8080

CMD ["python", "main.py"]