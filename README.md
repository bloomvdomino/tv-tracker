![TV Tracker](https://raw.githubusercontent.com/olivertso/tv-tracker/master/project/core/static/core/img/logo.png)

*Special thanks to [Tiago](https://github.com/tmazza) for providing our amazing logo* 🍺

[![GitHub tag](https://img.shields.io/github/tag/olivertso/tv-tracker.svg)](https://github.com/olivertso/tv-tracker)
[![Build Status](https://travis-ci.org/olivertso/tv-tracker.svg?branch=master)](https://travis-ci.org/olivertso/tv-tracker)
[![Coverage Status](https://coveralls.io/repos/github/olivertso/tv-tracker/badge.svg?branch=master)](https://coveralls.io/github/olivertso/tv-tracker?branch=master)

[TV-Tracker][tv-tracker] is a simple app that helps you track your favorite TV shows.

The app communicates with [TMDb API][tmdb-api] to fetch TV show data.

## Developing

### Requirements

- [Docker][docker]
- [Docker Compose][docker-compose]

### Useful Commands

Install images:
```
docker-compose build
```

Start services:
```
docker-compose up
```

Stop services and clean up containers:
```
docker-compose down
```

Run `manage.py` commands:
```
sh scripts/manage-py.sh <command>
```

Run linters:
```
sh scripts/lint.sh
```

Run tests:
```
sh scripts/test.sh
```

[docker]: https://www.docker.com/
[docker-compose]: https://docs.docker.com/compose/
[tmdb-api]: https://developers.themoviedb.org/3
[tv-tracker]: https://my-tv-tracker.herokuapp.com/
