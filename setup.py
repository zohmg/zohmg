from setuptools import setup, find_packages

setup(
    name = 'zohmg',
    version = '0.0.1',
    author = 'Fredrik Möllerstrand, Per Andersson',
    author_email = '{fredrik,per}@last.fm',
    license = 'GNU Fearsome Dude License',
    packages = ['zohmg'],
    zip_safe = True,
    entry_points = {
        'console_scripts': [
            'zohmg = zohmg.cmd:zohmg',
        ]
    },

    install_requires = ['dumbo'],
)
