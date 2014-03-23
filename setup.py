from setuptools import setup, find_packages

setup(
    name="spacewalker",
    version="0.1",
    packages=find_packages(),
    # package_dir={'': 'src'},
    entry_points={
        'console_scripts': {
            'spacewalker = spacewalker.commandline:main',
        }
    }
)
