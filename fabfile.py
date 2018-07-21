import re
from contextlib import contextmanager

from fabric.api import local


def lint():
    local('isort -rc project')
    local('flake8 --max-line-length=99 --exclude=migrations project')


@contextmanager
def switch_test_env():
    with open('.env', 'r') as file:
        original_env_content = file.read()

    original_env = re \
        .match(r'ENV=.*?\n', original_env_content) \
        .group(0) \
        .replace('\n', '') \
        .split('=')[1]

    test_env_content = re.sub(r'ENV=.*?\n', 'ENV=test\n', original_env_content)
    with open('.env', 'w') as file:
        file.write(test_env_content)
    print(f"Switched from {original_env} to test environment.")

    yield

    with open('.env', 'w') as file:
        file.write(original_env_content)
    print(f"Switched back to {original_env} environment.")


def coverage(module='project', html='html'):
    lint()
    with switch_test_env():
        local(f'coverage run manage.py test {module}')
        local(f'coverage {html}')


def test(module='project'):
    lint()
    with switch_test_env():
        local(f'./manage.py test {module}')
