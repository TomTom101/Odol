try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Ambient Light Sensor connected to Arduino',
    'author': 'Thomas Brandl',
    'author_email': 'thobra@gmail.com',
    'version': '0.22',
    'install_requires': ['nose', 'python-eeml', 'pyserial', 'facebook-sdk', 'numpy'],
    'packages': ['odol', 'tests'],
    'scripts': ['scripts/odol-service.py', 'www/odol-server.py', 'scripts/odol-draw.py'],
    'name': 'odol'
}

setup(**config)