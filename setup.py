from setuptools import setup, find_packages
import os

version = '0.3.1dev'

setup(name='Products.ZMIntrospection',
      version=version,
      description="Append an Introspection tab to an object's management tabs.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        'Framework :: Zope2',
        'Intended Audience :: Developers',
        ],
      keywords='',
      author='Stefane Fermigier',
      author_email='sf@nuxeo.com',
      url='http://www.nuxeo.com/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      )
