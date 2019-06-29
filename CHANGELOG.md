# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Last aired episode in progress card.

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
