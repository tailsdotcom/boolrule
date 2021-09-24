from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'pyparsing'
]

test_requirements = [
    'pytest'
]

setup(
    name='boolrule',
    version='0.3.4',
    description="Simple boolean expression evaluation engine",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',
    author="Steve Webster",
    author_email='spjwebster@gmail.com',
    url='https://github.com/tailsdotcom/boolrule',
    packages=[
        'boolrule',
    ],
    package_dir={'boolrule':
                 'boolrule'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='boolrule boolean expression',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Text Processing :: General',
    ],
)
