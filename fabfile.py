import re

from fabric.api import local


class SwitchEnv:
    def __init__(self):
        self.file_name = '.env'
        self.switch = False
        self.original_env = ''
        self.original_content = ''

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            try:
                self.get_original_content()
                self.get_original_env()
                if self.switch:
                    self.switch_to_test_env()
                func(*args, **kwargs)
            finally:
                if self.switch:
                    self.switch_to_original_env()
        return wrapper

    def get_original_content(self):
        with open(self.file_name, 'r') as file:
            self.original_content = file.read()

    def get_original_env(self):
        self.original_env = re.match(r'ENV=.*?\n', self.original_content).group(0)[4:-1]
        self.switch = self.original_env != 'test'

    def switch_to_test_env(self):
        new_content = re.sub(r'ENV=.*?\n', 'ENV=test\n', self.original_content)
        with open(self.file_name, 'w') as file:
            file.write(new_content)
        print(f"Switching from {self.original_env} to test environment.")

    def switch_to_original_env(self):
        with open(self.file_name, 'w') as file:
            file.write(self.original_content)
        print(f"Switching back from test to {self.original_env} environment.")


def lint():
    local('isort -rc project')
    local('flake8 --max-line-length=99 --exclude=migrations project')


@SwitchEnv()
def coverage(module='project', html='html'):
    lint()
    local(f'coverage run manage.py test {module}')
    local(f'coverage {html}')


@SwitchEnv()
def test(module='project'):
    lint()
    local(f'./manage.py test {module}')
