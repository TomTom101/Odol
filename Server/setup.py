try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Ambient Light Sensor connected to Arduino',
    'author': 'Thomas Brandl',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'thobra@gmail.com',
    'version': '0.1',
    'install_requires': ['nose', 'python-eeml', 'pyserial'],
    'packages': ['odol', 'tests'],
    'scripts': ['scripts/drawDaymage.py'],
    'name': 'odol'
}

setup(**config)