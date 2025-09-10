from setuptools import setup, find_packages

setup(
    name="career_assistant",       # Name on PyPI
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pdfplumber",
        "fastapi",
        "uvicorn"
    ],
    python_requires='>=3.9',
    description="A career assistant Python module",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="youremail@example.com",
    url="https://github.com/Sksanjay03/project",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
