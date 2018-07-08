from fabric.api import local


def lint():
    local('isort -rc project')
    local('flake8 --max-line-length=99 --exclude=migrations project')


def coverage(module='project', html='html', travis=''):
    lint()
    env = 'travis' if travis == 'travis' else 'test'
    local(f'coverage run manage.py test --settings=project.settings.{env} {module}')
    local(f'coverage {html}')


def test(module='project'):
    lint()
    local(f'./manage.py test --settings=project.settings.test {module}')
