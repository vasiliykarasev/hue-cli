import os
from setuptools import setup

setup(
    name = "hue cli",
    version = "0.0.1",
    author_email = "karasev00@gmail.com",
    description = ("Hue CLI"),
    license = "GPL",
    scripts = ['hue'],
    install_requires=["phue"],
)
