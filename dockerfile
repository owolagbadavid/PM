
ARG PYTHON_VERSION=3.11.2
FROM python:${PYTHON_VERSION}-slim as base

WORKDIR /app

COPY . .

# Expose the port that the application listens on.
EXPOSE 5000

#install required packages
RUN pip install -r requirements.txt

# Run the application.
CMD ./start.sh


