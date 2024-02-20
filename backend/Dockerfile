# Base image
FROM python:3.11-slim

# Get Build Arguments
ARG OPENAI_API_KEY
ARG FRONTEND_API_PASS
ARG API_AUTH_ENABLED
ARG MONGO_DB_USER
ARG MONGO_DB_PASS

# Set working directory
WORKDIR /app

# Copy package requires and install through pip
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copy all project files
COPY . .

# Create env file with necessary values
# Create Local Environment Variables
RUN touch .env
RUN echo "OPENAI_API_KEY=$OPENAI_API_KEY\nFRONTEND_API_PASS=$FRONTEND_API_PASS\nAPI_AUTH_ENABLED=$API_AUTH_ENABLED\nMONGO_DB_USER=$MONGO_DB_USER\nMONGO_DB_PASS=$MONGO_DB_PASS" > .env

# Executables
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]