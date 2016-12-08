from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='copper',
    version='0.1',
    description='Pipeline infrastructure for data processing.',
    long_description=readme(),

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    keywords='processing pipeline',

    url='https://github.com/ucdrascal/copper',
    author='Kenneth Lyons',
    author_email='ixjlyons@gmail.com',
    license='MIT',

    packages=['copper'],

    test_suite='nose.collector',
    tests_require=['nose'],
)
