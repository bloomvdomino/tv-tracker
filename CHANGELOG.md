# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Resource reservations #21
- Deploy using travis #23

### Changed
- Release checklist #22
- Split lint-n-format.sh #24

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

[Unreleased]: https://github.com/olivertso/tv-tracker/compare/2.11.0...HEAD
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
