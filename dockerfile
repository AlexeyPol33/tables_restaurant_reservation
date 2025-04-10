FROM python:3.12.9

ENV PYTHONUNBUFFERED=1
ENV DEBUG=0
ENV DB_NAME=tables_reservations
ENV DB_USER=postgres
ENV DB_PASSWORD=postgres
ENV DB_HOST=db
ENV DB_PORT=5432

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD alembic upgrade head && python ./app/main.py