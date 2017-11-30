from setuptools import setup
from setuptools import find_packages


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='pydaemo',
      version='0.1',
      description='Python wrapper for Daemo: a crowdsourcing platform.',
      url='http://github.com/ranjaykrishna/pydaemo',
      author='Ranjay Krishna',
      author_email='ranjaykrishna@gmail.com',
      license='MIT',
      packages=['pydaemo'],
      zip_safe=False,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      include_package_data=True)
