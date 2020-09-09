from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='WAPT Tools',
    url='https://github.com/lrobinot/wapt-tools',
    author='Ludovic ROBINOT',
    author_email='lrobinot@gmail.com',
    packages=['wapttools'],
    install_requires=['beautifulsoup4', 'requests'],
    version='0.1',
    license='Apache 2.0',
    description='WAPT modules to ease version upgrades.',
)
