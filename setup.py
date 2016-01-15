from distutils.core import setup

with open("README.md", "r") as fp:
    long_description = fp.read()

version = "0.5.10"

setup(name="catanlog",
      version=version,
      author="Ross Anderson",
      author_email="ross.anderson@ualberta.ca",
      url="https://github.com/rosshamish/catanlog/",
      download_url = 'https://github.com/rosshamish/catanlog/tarball/'+version,
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
