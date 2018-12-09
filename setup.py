#!/usr/bin/python3
from setuptools import find_packages
from distutils.core import setup

version = "0.1"

setup(name='drawmcskin',
      version=version,
      author="Andrey Lebedev",
      author_email="andrey@lebedev.lt",
      url="https://github.com/kedder/drawmcskin",
      description=("Convert hand drawing to minecraft skin"),
      license="GPLv3",
      keywords=["minecraft", "opencv"],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 3',
          'Natural Language :: English',
          'Topic :: Utilities',
          'Environment :: Console',
          'Operating System :: OS Independent',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
      packages=find_packages('src'),
      package_dir={'': 'src'},
      entry_points={
          'console_scripts':
          ['drawmcskin = drawmcskin.drawmcskin:main'],
        },
      include_package_data=True,
      )