from setuptools import setup, find_packages

setup(
    name="vokindle",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4>=4.12.3",
        "translate>=3.6.1",
        "libretranslatepy>=2.1.1",
        "tqdm>=4.66.1"
    ],
    entry_points={
        'console_scripts': [
            'vokindle=vokindle.cli:main',
        ],
    },
    author="Robin Köstler",
    author_email="your.email@example.com",
    description="A tool to extract vocabulary (with translations) and quotes from Kindle HTML exports",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/robinkoestler/vokindle",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 