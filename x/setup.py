from setuptools import setup
from setuptools import find_packages

setup(
    name='letsencrypt-combined',
    description="Installed combined certificates to a directory.",
    url='https://github.com/nickbreen/letsencrypt-combined-installer',
    author="Nick Breen",
    author_email='nick@foobar.net.nz',
    license='Apache License 2.0',
    install_requires=[
        'letsencrypt',
        'zope.interface',
    ],
    packages=find_packages(),
    entry_points={
        'letsencrypt.plugins': [
            'combined = letsencrypt_combined.combined:Installer',
        ],
    },
)
