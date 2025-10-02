# Use Python 3.10 slim image as the base
FROM python:3.10.8-slim

# Set working directory inside the container
WORKDIR /code

# Copy pyproject.toml and poetry.lock into the container
COPY ./pyproject.toml ./poetry.lock* /code/

# Install dependencies using Poetry
RUN pip install --no-cache-dir poetry

# Install project dependencies using poetry
RUN poetry config virtualenvs.create false && poetry install

# Copy the entire source code into the container
COPY . /code/

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI app using Uvicorn with Poetry
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
