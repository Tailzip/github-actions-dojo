FROM python:alpine
LABEL maintainer="T Ki"

ARG APP_VERSION
ENV APP_VERSION=$APP_VERSION

# Create and change working directory
WORKDIR /app
# Add application requirements
COPY requirements.txt .
# Install requirements
RUN pip install --no-cache-dir -r requirements.txt
# Add application
COPY app.py .
# Create a specific user to run the Python application
RUN adduser -D my-user -u 1000

USER 1000

EXPOSE 8000

# Launch application
ENTRYPOINT ["gunicorn"]
CMD ["-b", "0.0.0.0:8000", "app:APP"]
