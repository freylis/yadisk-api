import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()


setup(
    name='yadisk-api',
    version='1.0.1',
    packages=['yadisk_api'],
    url='https://github.com/freylis/yadisk-api',
    license='MIT License',
    author='Mikhail Volkov',
    author_email='freylis2@gmail.com',
    description='Yandex.disk http api client',
    long_description=README,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries',
    ],
    install_requires = [
        'requests >= 2.9.1',
    ],
)
