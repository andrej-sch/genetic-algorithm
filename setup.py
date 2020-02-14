import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="genetic-algorithm-pkg-andrej-sch", # Replace with your own username
    version="0.0.1",
    author="andrej-sch",
    author_email="r335988@gmail.com",
    description="A genetic algorithm for unconstrained single-objective optimization problems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andrej-sch/genetic-algorithm",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    test_suite="tests.tests"
)
