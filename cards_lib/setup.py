from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='cardlib',
  version='0.0.1',
  author='sofi-pbor',
  author_email='sofi-pbor@ya.ru',
  description='Simple graphic library for creating cards for words',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/Coun7Z3ro',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='cards interface',
  project_urls={
    'GitHub': 'https://github.com/Coun7Z3ro'
  },
  python_requires='>=3.6'
)

