[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=tanthana48_softenghw1&metric=coverage)](https://sonarcloud.io/summary/new_code?id=tanthana48_softenghw1)

[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=tanthana48_softenghw1&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=tanthana48_softenghw1)

[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=tanthana48_softenghw1&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=tanthana48_softenghw1)

[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=tanthana48_softenghw1&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=tanthana48_softenghw1)

## Setup Instruction
```
poetry install
```

## Run Test
```
poetry run pytest
```

## What to do next

### Install Pre-commit (Recommended)
```
poetry run pre-commit install
```
If you wish to edit pre-commit behavior see ```.pre-commit-config.yaml```.
Normally it checks only the file you are committing. But if you wish to run it manually for all files do
```
poetry run pre-commit run --all
```

### Run docker
```
docker run --name vending_machine -e POSTGRES_PASSWORD={password} -p 5432:5432 -d postgres
```

### Adjusting the Postgres
edit app.py
```
"postgresql://postgres:{password}@localhost:5432/vending_machine"
```

### Create Database
```CREATE DATABASE "vending_machine";```

### Finish!! You can try now
