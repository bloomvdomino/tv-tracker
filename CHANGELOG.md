# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Changed
- Use `olivertso/pip-tools` docker image #124
- Rename directory project to source #125

## [2.29.0] - 2020-04-19
### Changed
- UI improvements (card radius, shadow, loader) #122

## [2.28.0] - 2020-04-19
### Added
- Add dark theme #120

### Changed
- Allow running `bin/test` with different users #116
- Update requirements #117
- Separate pip-tools to its own Dockerfile #118
- Use python-slim docker image #119

### Removed
- `shfmt` #116

## [2.27.0] - 2020-02-23
### Changed
- Remove trailing slash from TMDB_API_URL #107
- Replace poetry by pip-tools #110

### Fixed
- Stop running tests as root user in CI #113
- Fix coverage hack in CI #114

### Security
- Bump django version from 3.0.2 to 3.0.3 #112

## [2.26.0] - 2020-01-26
### Added
- Shell script for poetry #101

### Changed
- Use poetry #95
- Make shell scripts executable #96
- Refactor .travis.yml #97
- Run docker as root user in travis instead of docker compose #100
- Shell script chores #103
- Upgrade black #104
- Upgrade httpx #105

### Fixed
- Travis deploy #102

## [2.25.1] - 2020-01-05
### Fixed
- Do not treat 404 as error when updating progresses #93

## [2.25.0] - 2020-01-04
### Added
- Capture exceptions when updating progresses #89

### Changed
- Bump python to 3.8 #90
- Update dependencies and tools #91

## [2.24.0] - 2020-01-01
### Changed
- Bump django version to 3.0.1 #87

## [2.23.0] - 2019-11-30
### Added
- Docker multi-stage builds #80

### Changed
- Optimize docker image caching #79
- Improve .dockerignore #81
- Use gunicorn as development server #82
- Improve .dockerignore #83
- Update dependencies #84

### Fixed
- Apk ignoring apkindex warning #83

## [2.22.0] - 2019-10-22
### Added
- Display newest episode of paused and stopped shows #77

### Changed
- Replace format by f-string #76

## [2.21.0] - 2019-10-13
### Changed
- Do not raise exception when updating progresses #72
- Update pip requirements #73
- Replace requests with httpx #74

### Removed
- Health check endpoint #71

## [2.20.0] - 2019-10-05
### Changed
- Refactor update_progresses command #69

### Removed
- LogDNA addon #68

### Fixed
- `update_progresses` command #67

## [2.19.0] - 2019-10-04
### Added
- Shell formatter (`shfmt`) and Dockerfile linter (`hadolint`) #59
- `update_progresses` command #60
- LogDNA addon #64
- Scheduler addon #65

### Changed
- Save show name by language #58
- Use absolute imports #61

## [2.18.0] - 2019-09-28
### Added
- Backup database before deploying on production #52
- Sentry #55

### Changed
- Update python version to 3.7.4 #51
- Change from email to `noreply@tv-tracker<-env>.com` #53

### Removed
- `django-suit` #54
- Error reports by email #56

### Security
- Docker login with --password-stdin #50

## [2.17.1] - 2019-09-21
### Fixed
- Production deploy #47

## [2.17.0] - 2019-09-21
### Added
- QA to CI #45

### Changed
- Update pip dependencies #42
- Add terraform to docker image #44

### Removed
- `apps_emails` app #41

### Fixed
- Terraform 0.12 in CI #43

## [2.16.0] - 2019-09-01
### Removed
- `SendGridEmail` model #39

## [2.15.0] - 2019-09-01
### Changed
- Migrate to Heroku #37

## [2.14.1] - 2019-08-28
### Changed
- Update health check endpoint in terraform #34

### Fixed
- `get_air_date` returning empty string #35

## [2.14.0] - 2019-08-11
### Fixed
- Deploy script #32

## [2.13.0] - 2019-08-11
### Added
- Health check endpoint #30

### Changed
- Use double quotes in deploy.sh #28
- Migrate to terraform 0.12 #29

### Security
- Update dependencies #27

## [2.12.0] - 2019-07-28
### Added
- Resource reservations #21
- Deploy using travis #23

### Changed
- Release checklist #22
- Split lint-n-format.sh #24

### Security
- Dockerfile non-root user #25

## [2.11.0] - 2019-07-21
### Changed
- Use aws-ecs-app module. #19

## [2.10.0] - 2019-07-07
### Added
- Update show data on progress page load. #12
- Update show data when clicking next button. #14
- Release checklist. #16

### Changed
- Refactor clean_last_watched. #15

### Removed
- flake8 noqa. #11

### Fixed
- Release checklist. #17

### Security
- Upgrade dependencies. #13

## [2.9.0] - 2019-07-01
### Added
- Clean up unused Docker data after app init. #8

### Fixed
- `get_air_date` KeyError. #7

### Security
- Enforce CSRF protection in AJAX requests. #6
- Use Bandit. #9

## [2.8.0] - 2019-06-29
### Added
- Last aired episode in progress card.
- Progress delete button in progress page. #2
- Error reporting via email. #4

### Changed
- Move isort config to pyproject.toml. #3

## [2.7.0] - 2019-06-24
### Added
- Travis stages.

### Changed
- Disable travis on success email notification.

### Removed
- jQuery used by the next button.

## [2.6.0] - 2019-06-22
### Added
- Next button in progress card.

## [2.5.0] - 2019-06-21
### Added
- Automagic deploy on tag creation.

### Security
- Update pip dependencies.

## [2.4.0] - 2019-06-15
### Changed
- Database backups folder directory.
- Use hobby-infra as the infrastructure.

## [2.3.0] - 2019-04-28
### Added
- Terraform linting in Travis.
- Black formatting.
- Custom domain.
- Database backup.

### Changed
- Increase posters sizes.
- Use Terraform remote state with S3.
- Use gevent gunicorn worker.
- Migrate from Heroku to AWS.

## [2.2.2] - 2019-03-26
### Fixed
- Non-started paused progress being saved as finished.

## [2.2.1] - 2019-03-23
### Fixed
- Time zone not saved on signup.

## [2.2.0] - 2019-03-21
### Added
- Local HTML coverage report.
- `_Show` class.
- Developing section in `README.md`.

### Changed
- Change cached_property to property of `_Show.status_display`.
- Refactor `_Show.status_value`.
- Titlelize labels.

### Fixed
- TMDb API of episode detail may return results without air date.

## [2.1.0] - 2019-03-16
### Added
- Time zone support (fix progress next air date issue).
- Code coverage.
- Progresses page section links.

### Changed
- Update existing tests to use pytest.
- Use Roboto for font family.

### Fixed
- Season with more than 99 episodes.

## [2.0.3] - 2019-03-10
### Fixed
- Heroku command app option.

## [2.0.2] - 2019-03-10
### Fixed
- Badge links in `README.md`.

## [2.0.1] - 2019-03-10
### Fixed
- Heroku app name.

## [2.0.0] - 2019-03-10
### Changed
- Migrate from an API to a full-stack app.

[Unreleased]: https://github.com/olivertso/tv-tracker/compare/2.29.0...HEAD
[2.29.0]: https://github.com/olivertso/tv-tracker/compare/2.28.0...2.29.0
[2.28.0]: https://github.com/olivertso/tv-tracker/compare/2.27.0...2.28.0
[2.27.0]: https://github.com/olivertso/tv-tracker/compare/2.26.0...2.27.0
[2.26.0]: https://github.com/olivertso/tv-tracker/compare/2.25.1...2.26.0
[2.25.1]: https://github.com/olivertso/tv-tracker/compare/2.25.0...2.25.1
[2.25.0]: https://github.com/olivertso/tv-tracker/compare/2.24.0...2.25.0
[2.24.0]: https://github.com/olivertso/tv-tracker/compare/2.23.0...2.24.0
[2.23.0]: https://github.com/olivertso/tv-tracker/compare/2.22.0...2.23.0
[2.22.0]: https://github.com/olivertso/tv-tracker/compare/2.21.0...2.22.0
[2.21.0]: https://github.com/olivertso/tv-tracker/compare/2.20.0...2.21.0
[2.20.0]: https://github.com/olivertso/tv-tracker/compare/2.19.0...2.20.0
[2.19.0]: https://github.com/olivertso/tv-tracker/compare/2.18.0...2.19.0
[2.18.0]: https://github.com/olivertso/tv-tracker/compare/2.17.1...2.18.0
[2.17.1]: https://github.com/olivertso/tv-tracker/compare/2.17.0...2.17.1
[2.17.0]: https://github.com/olivertso/tv-tracker/compare/2.16.0...2.17.0
[2.16.0]: https://github.com/olivertso/tv-tracker/compare/2.15.0...2.16.0
[2.15.0]: https://github.com/olivertso/tv-tracker/compare/2.14.1...2.15.0
[2.14.1]: https://github.com/olivertso/tv-tracker/compare/2.14.0...2.14.1
[2.14.0]: https://github.com/olivertso/tv-tracker/compare/2.13.0...2.14.0
[2.13.0]: https://github.com/olivertso/tv-tracker/compare/2.12.0...2.13.0
[2.12.0]: https://github.com/olivertso/tv-tracker/compare/2.11.0...2.12.0
[2.11.0]: https://github.com/olivertso/tv-tracker/compare/2.10.0...2.11.0
[2.10.0]: https://github.com/olivertso/tv-tracker/compare/2.9.0...2.10.0
[2.9.0]: https://github.com/olivertso/tv-tracker/compare/2.8.0...2.9.0
[2.8.0]: https://github.com/olivertso/tv-tracker/compare/2.7.0...2.8.0
[2.7.0]: https://github.com/olivertso/tv-tracker/compare/2.6.0...2.7.0
[2.6.0]: https://github.com/olivertso/tv-tracker/compare/2.5.0...2.6.0
[2.5.0]: https://github.com/olivertso/tv-tracker/compare/2.4.0...2.5.0
[2.4.0]: https://github.com/olivertso/tv-tracker/compare/2.3.0...2.4.0
[2.3.0]: https://github.com/olivertso/tv-tracker/compare/2.2.2...2.3.0
[2.2.2]: https://github.com/olivertso/tv-tracker/compare/2.2.1...2.2.2
[2.2.1]: https://github.com/olivertso/tv-tracker/compare/2.2.0...2.2.1
[2.2.0]: https://github.com/olivertso/tv-tracker/compare/2.1.0...2.2.0
[2.1.0]: https://github.com/olivertso/tv-tracker/compare/2.0.3...2.1.0
[2.0.3]: https://github.com/olivertso/tv-tracker/compare/2.0.2...2.0.3
[2.0.2]: https://github.com/olivertso/tv-tracker/compare/2.0.1...2.0.2
[2.0.1]: https://github.com/olivertso/tv-tracker/compare/2.0.0...2.0.1
[2.0.0]: https://github.com/olivertso/tv-tracker/compare/1.5.3...2.0.0
