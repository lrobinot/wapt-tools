from setuptools import setup, find_packages

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='wapt_tools',
    url='https://github.com/lrobinot/wapt-tools',
    author='Ludovic ROBINOT',
    author_email='lrobinot@gmail.com',
    packages=find_packages(),
    install_requires=['beautifulsoup4', 'requests'],
    version='0.5',
    license='Apache 2.0',
    description='WAPT modules to ease version upgrades.',
)
