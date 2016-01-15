from distutils.core import setup

import catanlog

with open("README.md", "r") as fp:
    long_description = fp.read()

setup(name="catanlog",
      version=catanlog.__version__,
      author="Ross Anderson",
      author_email="ross.anderson@ualberta.ca",
      url="https://github.com/rosshamish/catanlog/",
      download_url = 'https://github.com/rosshamish/catanlog/tarball/' + catanlog.__version__,
      description="reference implementation for the catanlog (.catan) file format",
      long_description=long_description,
      keywords=[],
      classifiers=[],
      license="GPLv3",

      py_modules=["catanlog"],
      install_requires=[
          'hexgrid',
      ],
	)
