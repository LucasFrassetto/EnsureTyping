from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="EnsureTyping",
    version="0.0.1",
    author="Lucas de Angelo Frassetto",
    author_email="lucasfrassetto8@gmail.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    license_files=("LICENSE.txt"),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Typing :: Typed",
    ],
    install_requires=[],
    package_data={"ensure_typing":["*"]},
)
