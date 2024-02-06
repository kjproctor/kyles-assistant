FROM python:3.11-slim

ENV VAR1=10

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=OPENAI_API_KEY

WORKDIR /app
COPY backend .
COPY docs .
COPY langchain-doc-index .
COPY consts.py .
COPY ingestion.py .
COPY main.py .
COPY Pipfile .
COPY Pipfile.lock .

RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy

# Creates a non-root user and adds permission to access the /app folder
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Streamlit default port
EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "main.py", "--server.address", "0.0.0.0", "--server.port", "8501"]
