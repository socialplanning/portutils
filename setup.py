from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='portutils',
      version=version,
      description="Find processes given a port number and kill them",
      long_description="""
this is basically a front-end to netstat that will find processes
given a port number (portcheck) and kill them (portkill)      
""",
      classifiers=[],
      keywords='opencore',
      author='Jeff Hammel',
      author_email='opencore-dev at lists.coactivate.org',
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
