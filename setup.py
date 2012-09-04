
from setuptools import setup
from dot-pixel import version

setup(
	name = 'dot-pixel',
	version = version,
	description = 'TODO',
	author = "None",
	author_email = "None",
	scripts = ['dot-pixel.py'],
	packages = ['dot-pixel'],
	install_requires = ["setuptools", 'svgwrite', 'PIL'])
