import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="voc-xml", # Replace with your own username
    version="0.0.1",
    author="Jason Li",
    author_email="lzzduke06@gmail.com",
    description="Package to generate and modify VOC label files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JasonDoingGreat/voc_xml",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)