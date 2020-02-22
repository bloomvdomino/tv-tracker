![TV Tracker](https://raw.githubusercontent.com/olivertso/tv-tracker/master/project/core/static/core/img/logo.png)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Build Status](https://travis-ci.org/olivertso/tv-tracker.svg?branch=master)](https://travis-ci.org/olivertso/tv-tracker)
[![Coverage Status](https://coveralls.io/repos/github/olivertso/tv-tracker/badge.svg?branch=master)](https://coveralls.io/github/olivertso/tv-tracker?branch=master)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/olivertso/tv-tracker)

TV-Tracker is a simple app that helps you to track your favorite TV shows.

The app fetches TV show data from [TMDb API][tmdb-api].

*Special thanks to [Tiago](https://github.com/tmazza) for providing our amazing logo* 🍺

## Development

Create `.env` file:
```
cp .env.example .env
```

Issue a TMDb API key [here][tmdb-api] and update `TMDB_API_KEY` in `.env` file.

Build the image:
```
docker-compose build
```

Run the application at http://localhost:8000:
```
docker-compose up
```

### Useful commands

Run `manage.py` commands:
```
bin/manage-py <command>
```

Run code formatters:
```
bin/format
```

Run code linters:
```
bin/lint
```

Run tests:
```
bin/test
```

Upgrade packages
```
bin/pip-upgrade
```

[tmdb-api]: https://developers.themoviedb.org/3/getting-started/introduction
