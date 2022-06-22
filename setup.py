import io

from setuptools import setup


version = '0.99a1'


with io.open('README.md', encoding='utf8') as readme:
    long_description = readme.read()


setup(
    name='sample',
    version=version,
    package_dir={'': 'sample'},
    description='Code Sample.',
    long_description=long_description,
    author='Francis Gauthier',
    author_email='francisgauthier1@gmail.com    ',
    url='https://github.com/fjgauthier',
    install_requires=[
        'numpy==1.22.0',
    ],
    extras_require={},
    license='New BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development',
    ],
)
