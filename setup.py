import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="appengine-python-standard",
    version="0.0.1a1",
    author="Google LLC",
    description="Google App Engine Python 3 Standard Environment API library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GoogleCloudPlatform/appengine-python-standard",
    packages=setuptools.find_packages(where="src"),
    namespace_packages=["google"],
    package_dir={"": "src"},
    install_requires=[
        "protobuf>=3.14.0",
        "ruamel.yaml>=0.15,<0.16",
        "six>=1.15.0",
        "urllib3>=1.26.2,<2",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6, <4",
)
