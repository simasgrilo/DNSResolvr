FROM python:3.10.15
WORKDIR /app
RUN pip install -U pip
RUN apt-get update
RUN pip install poetry
RUN python -m venv /venv
COPY . /app/
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --no-root
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]