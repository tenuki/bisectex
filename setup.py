from setuptools import setup, find_packages

VERSION = '0.0.3'
DESCRIPTION = 'Bisect module also supporting functions'
LONG_DESCRIPTION = 'Bisect module supporting functions like: bisectf(lambda x: (x**2)-2 < 0, 0, 10, 0.000000001)'

setup(
    name="bisectex",
    version=VERSION,
    author="david weil",
    author_email="<david.weil@coinfabrik.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    py_modules=['bisectex'],
    keywords=['python', 'bisect', 'bisect-function', 'bisectex'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
