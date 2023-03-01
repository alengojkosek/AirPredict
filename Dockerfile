FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install poetry && poetry install

EXPOSE 44933

CMD ["poetry", "run", "python", "src/serve/api.py"]
