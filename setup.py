from setuptools import setup, find_packages

setup(
    name='gigpy',
    version='0.1',
    author='Brendan Griffen',
    author_email='brendan.f.griffen@gmail.com',
    url='https://github.com/bgriffen/gigpy',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4',
        'spotipy',
        'requests',
        'PyYAML',
        'pandas',
    ],
)
