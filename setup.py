from setuptools import setup

setup(name='kurator',
      version='0.3',
      description='Command line tool to help with media dumps',
      keywords=['media', 'dump', 'file', 'transfer', 'exif', 'photos', 'images', 'duplicate', 'rename'],
      url='http://github.com/saltycatfish/kurator',
      download_url='https://github.com/saltycatfish/kurator/archive/0.3.tar.gz',
      author='SaltyCatFish',
      author_email='ryan@saltycatfish.com',
      license='MIT',
      packages=['kurator', 'kurator.lib'],
      install_requires=[
          'attrs==17.4.0',
          'colorama==0.3.9',
          'ExifRead==2.1.2',
          'more-itertools==4.1.0',
          'pluggy==0.6.0',
          'py==1.5.3',
          'pytest==3.5.0',
          'six==1.11.0',
          'click==6.7',
      ],
      entry_points={
          'console_scripts': ['kurator=kurator.command_line:main'],
      },
      zip_safe=False)
