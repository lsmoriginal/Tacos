import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Tacos",
    version="0.0.1",
    author="ShaoMin Liu",
    author_email="liushaomin2@gmail.com",
    description="Simple wrappers for some commonly use functionalities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lsmoriginal/Tacos",
    packages=setuptools.find_packages(),
    package_data={
        '':['*.json', '*.csv', "*.dic", "*.aff"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "Pillow",
        "Pandas",
        "pytz",
        "pyyaml",
        # "pynvml",
        # "psutil",
    ],
    python_requires='>=3.6'
)
