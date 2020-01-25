![TV Tracker](https://raw.githubusercontent.com/olivertso/tv-tracker/master/project/core/static/core/img/logo.png)

![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/olivertso/tv-tracker)
[![Build Status](https://travis-ci.org/olivertso/tv-tracker.svg?branch=master)](https://travis-ci.org/olivertso/tv-tracker)
[![Coverage Status](https://coveralls.io/repos/github/olivertso/tv-tracker/badge.svg?branch=master)](https://coveralls.io/github/olivertso/tv-tracker?branch=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

TV-Tracker is a simple app that helps you to track your favorite TV shows.

The app fetches TV show data from [TMDb API][tmdb-api].

*Special thanks to [Tiago](https://github.com/tmazza) for providing our amazing logo* 🍺

## Development

### Useful commands

Build the image:
```
docker-compose build
```

Start services (Django server at http://localhost:8000):
```
docker-compose up
```

Stop services and clean up containers:
```
docker-compose down
```

Run `manage.py` commands:
```
scripts/manage-py <command>
```

Run tests:
```
scripts/test
```

Run code formatters:
```
scripts/format
```

Run code linters:
```
scripts/lint
```

### Upgrade PIP packages

1. Update package version(s) in `pyproject.toml`.
2. Update `poetry.lock`: `scripts/poetry lock`.
3. Rebuild the image: `docker-compose build`.

## Release

- [ ] Checkout to `master` branch.
- [ ] Pull changes.
- [ ] Checkout to a new branch `release/x.x.x`.
- [ ] Update `CHANGELOG.md`.
  - [ ] Add a blank line and `## [x.x.x] - YYYY-MM-DD` bellow `## [Unreleased]`.
  - [ ] Update compare links at the bottom section.
- [ ] Commit with message `Release x.x.x` and push.
- [ ] Open and merge a PR with title `Release x.x.x`.
- [ ] Delete branch `release/x.x.x`.
- [ ] Checkout to `master` branch.
- [ ] Pull changes.
- [ ] Create a tag `x.x.x`.
- [ ] Push the tag.
- [ ] Create a release with title `x.x.x`.
  - [ ] Copy and paste the newest section from `CHANGELOG.md` to the release description.

## Deploy

Creating a tag will trigger an automagic deploy from Travis.

[tmdb-api]: https://developers.themoviedb.org/3
