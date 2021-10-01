import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="appengine-python-standard",
    version="0.2.2",
    author="Google LLC",
    description="Google App Engine services SDK for Python 3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GoogleCloudPlatform/appengine-python-standard",
    packages=setuptools.find_packages(where="src"),
    namespace_packages=["google"],
    package_dir={"": "src"},
    install_requires=[
        "frozendict>=1.2",
        "google-auth>=1.31.0",
        "mock>=4.0.3",
        "Pillow>=8.3.1",
        "protobuf>=3.18.0",
        "pytz>=2021.1",
        "requests>=2.25.1",
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
