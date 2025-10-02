## Project Setup Using Docker Compose

In the root of the project run the following command to build and start the services:

docker-compose -f src/docker-compose.yml up --build -d

## Access the FastAPI API

Once the services are up and running, you can access the FastAPI documentation and interact with the API:

FastAPI API Docs: http://localhost:8000/api/v1/docs

Here, you'll find the Swagger UI where you can test the API endpoints.