![TV Tracker](https://raw.githubusercontent.com/olivertso/tv-tracker/master/project/core/static/core/img/logo.png)

[![GitHub tag](https://img.shields.io/github/tag/olivertso/tv-tracker.svg)](https://github.com/olivertso/tv-tracker)
[![Build Status](https://travis-ci.org/olivertso/tv-tracker.svg?branch=master)](https://travis-ci.org/olivertso/tv-tracker)
[![Coverage Status](https://coveralls.io/repos/github/olivertso/tv-tracker/badge.svg?branch=master)](https://coveralls.io/github/olivertso/tv-tracker?branch=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

TV-Tracker is a simple app that helps you track your favorite TV shows.

The app communicates with [TMDb API][tmdb-api] to fetch TV show data.

*Special thanks to [Tiago](https://github.com/tmazza) for providing our amazing logo* 🍺

## Development

### Requirements

- [AWS][aws]
- [Docker][docker]
- [Docker Compose][docker-compose]
- [Terraform][terraform]

### Application

Install images:
```
sh scripts/docker-compose.sh build
```

Start services (Django server at http://localhost:8000):
```
sh scripts/docker-compose.sh up
```

Stop services and clean up containers:
```
sh scripts/docker-compose.sh down
```

Run `manage.py` commands:
```
sh scripts/manage-py.sh <command>
```

Run tests:
```
sh scripts/test.sh
```

### Infrastructure

Develop and test the infrastructure in QA environment.

CD to QA directory:
```
cd terraform/qa/
```

Initialize local configuration files:
```
terraform init
```

Create or update the infrastructure:
```
terraform apply
```

Always destroy the infrastructure after developing/testing:
```
terraform destroy
```

### Other Commands

Run formatters:
```
sh scripts/format.sh [--check]
```

## Deploy

### Requirements

- [AWS][aws]
- [Docker][docker]
- [Terraform][terraform]

[aws]: https://aws.amazon.com/
[docker]: https://www.docker.com/
[docker-compose]: https://docs.docker.com/compose/
[terraform]: https://www.terraform.io/
[tmdb-api]: https://developers.themoviedb.org/3
