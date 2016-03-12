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
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ],
    keywords='processing pipeline',

    url='https://github.com/ixjlyons/copper',
    author='Kenneth Lyons',
    author_email='ixjlyons@gmail.com',
    license='new BSD',

    py_modules=['copper'],

    test_suite='nose.collector',
    tests_require=['nose'],
)
