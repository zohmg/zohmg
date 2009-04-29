from setuptools import setup, find_packages

setup(
    name = 'zohmg',
    version = '0.0.1',
    author = 'Fredrik Mollerstrand, Per Andersson',
    author_email = '{fredrik,per}@last.fm',
    license = 'GNU Fearsome Dude License',
    packages = ['zohmg'],
    zip_safe = False,
    entry_points = {
        'console_scripts': [
            'zohmg = zohmg.cmd:zohmg',
        ]
    },

    install_requires = ['dumbo'],
)
