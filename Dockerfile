FROM --platform=linux/arm64/v8 python:3.11.6-slim

# ENV PYTHONUNBUFFERED=1

# Update the system and install packages
RUN apt-get update -y \
    && pip install --upgrade pip \
    # dependencies for building Python packages
    && pip install --upgrade setuptools \
    && apt-get install -y build-essential \
    # install dependencies manager
    && pip install pipenv watchdog \
    # cleaning up unused files
    && rm -rf /var/lib/apt/lists/*


# Install project dependencies
COPY ./Pipfile ./Pipfile.lock /
RUN pipenv sync --system


# cd /app (get or create)
WORKDIR /app
COPY ./ ./

EXPOSE 8000

# RUN python src/manage.py runserver
# CMD sleep 2 && python src/manage.py runserver 0.0.0.0:8000

ENTRYPOINT [ "python" ]
CMD ["src/manage.py", "runserver", "0.0.0.0:8000"]
