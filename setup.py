
import os
from setuptools import setup

readme = os.path.join(os.path.dirname(__file__), 'README.rst')
LONG_DESCRIPTION = open(readme, 'r').read()

params = dict(
    name='apysigner',
    version='4.0.0',
    url='https://github.com/madisona/apysigner',
    license='BSD',
    author='Aaron Madison',
    author_email='aaron.l.madison@gmail.com',
    description='Basic API request signing',
    long_description=LONG_DESCRIPTION,
    py_modules=['apysigner'],

    zip_safe=False,
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
)

setup(**params)
