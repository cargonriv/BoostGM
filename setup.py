"""Utilities for setuptools integration."""
from setuptools import find_packages, setup


setup(
    name="BoostGM",
    version="0.0.1",
    description="NBA Boost Fantasy GM.",
    author="Carlos F. Gonzalez Rivera",
    author_email="cargonriv@gmail.com",
    packages=["boost_gm"]
)