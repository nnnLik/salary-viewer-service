FROM python:3.10-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /usr/src/app/

RUN pip install poetry
RUN poetry config virtualenvs.create false

EXPOSE 80

CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "--port", "80", "main:app"]
