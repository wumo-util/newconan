from setuptools import setup

with open("README.md", encoding='utf-8', mode='r') as fh:
    long_description = fh.read()

setup(name='newconan',
      version='2.6',
      description='New cmake project based on conan',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/wumo-util/newconan',
      author='wumo',
      license='MIT',
      packages=['newconan'],
      entry_points={
          'console_scripts': ['newconan=newconan.newconan:main'],
      },
      install_requires=[
          'conan'
      ],
      python_requires='>=3.6',
      include_package_data=True,
      zip_safe=False)
