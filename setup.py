from setuptools import setup
from setuptools import find_packages


setup(
    name="carpet",
    version="1.0.0",
    description="Carpet helps Anthonk find wideos",
    url="https://github.com/3ok/carpet",
    classifiers=[
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
    ],
    python_requires=">=3.8",
    install_requires=["youtube_transcript_api"],
    packages=find_packages(),
    entry_points={"console_scripts": ["carpet = carpet.main:main"]},
)
