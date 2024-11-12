FROM python:3.10.15
WORKDIR /app
RUN pip install -U pip
RUN apt-get update
RUN pip install poetry
RUN python -m venv /venv
COPY . /app/
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi
EXPOSE 5000
CMD ["python", "main.py"]