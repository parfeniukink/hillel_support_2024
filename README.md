# About

This is the educational project for IT Hillel

# `pipenv` usage

The pipenv is used as a main package manager on the project. For more information please follow the [🔗 documentation](https://pipenv.pypa.io/en/latest/)

```sh
# Creating a new virtual environment
pipenv shell

# Creating a .lock file from Pipenv file
pipenv lock

# Installing dependencies from .lock file
pipenv sync
```



# 🐳 Deploy with Docker Compose

```sh
cp .env.default .env
docker compose build && docker compose up -d
```


### Some useful commands

```sh
# look for last 20 log lines and follow the stdout until Ctrl-C
docker compose logs --tail 20 -f api

# execute the command inside the container
docker compose exec api <command>
```