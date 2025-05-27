from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="navefileuploader",
    version="1.1.2",
    author="Amanda Varella",
    author_email="amandavarella@amanda.varella",
    description="A tool for masking and syncing JIRA data to Nave",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amandavarella/navefileuploader",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "nave-mask=navefileuploader.masking:main",
            "nave-sync=navefileuploader.sync:main",
        ],
    },
) 