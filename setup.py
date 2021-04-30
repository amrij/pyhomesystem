from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='pyhomesystem',
      version='0.10',
      description='Module to communicate with homesystem',
      long_description='Module to communicate with homesystem',
      url='https://github.com/amrij/pyhomesystem',
      classifiers=[
          'Development Status :: 1 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 3 :: Only',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      author='André Rijkeboer',
      author_email='root@am-rijkeboer.nl',
      license='Apache 2.0',
      packages=['pyhomesystem'],
      install_requires=[
          'aiohttp',
      ],
      include_package_data=True,
      zip_safe=False)
