from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='portutils',
      version=version,
      description="",
      long_description="""
this is basically a front-end to netstat that will find processes
given a port number (portcheck) and kill them (portkill)      
""",
      classifiers=[], # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      keywords='topp openplans',
      author='The Open Planning Project',
      author_email='jhammel@openplans.org',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      include_package_data=True,
      zip_safe=False,
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      portcheck = portutils:portcheck_main
      portkill = portutils:portkill_main
      """,
      )
