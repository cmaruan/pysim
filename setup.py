import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-sim", 
    version="0.1.5",
    author="Cristian Maruan Bosin",
    author_email="cmbosin@inf.ufpel.edu.br",
    description="Tool to run parametrized jobs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cmaruan/pysim",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)