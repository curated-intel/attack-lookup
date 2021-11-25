from setuptools import setup

with open("requirements.txt", "r") as f:
    deps = [x.strip() for x in f.readlines()]

setup(
    name="attack-lookup",
    version="1.0.0",
    description="MITRE ATT&CK Lookup Tool",
    url="",
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