import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rtedwards",  # Replace with your own username
    version="0.0.1",
    author="Robert Edwards",
    author_email="rtedwards.eng@gmail.com",
    description="An interactive dashboard for analyzing COVID-19 data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rtedwards/coronavirus-tracker",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
