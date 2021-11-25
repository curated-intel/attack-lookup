# https://github.com/realpython/reader/blob/master/setup.py

import pathlib

from setuptools import setup

base_dir = pathlib.Path(__file__).resolve().parent

with open(base_dir / "requirements.txt", "r") as f:
    deps = [x.strip() for x in f.readlines()]

with open(base_dir / "README.md", "r") as f:
    readme = f.read()

setup(
    name="attack-lookup",
    version="1.0.0",
    description="MITRE ATT&CK Lookup Tool",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/curated-intel/attack-lookup",
    author="Zander Work",
    author_email="pypi@zanderwork.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8"
    ],
    packages=["attack_lookup"],
    python_requires=">=3.6",
    include_package_data=True,
    install_requires=deps,
    entry_points={
        "console_scripts": [
            "attack-lookup=attack_lookup.__main__:main"
        ]
    }
)