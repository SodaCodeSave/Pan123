import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pan123",
    version="0.0.4",
    author="SodaCodeSave",
    author_email="soda_code@outlook.com",
    description="This is an unofficial 123 Pan Open Platform API library, which can easily call the 123 Pan Open Platform in Python without the need to write repetitive code multiple times",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SodaCodeSave/Pan123",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
