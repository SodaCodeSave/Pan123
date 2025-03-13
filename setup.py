import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pan123",
    version="0.1.4",
    author="SodaCodeSave&lixuehua",
    author_email="soda_code@outlook.com",
    description="非官方的123云盘Python包",
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
