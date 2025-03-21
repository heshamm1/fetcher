from setuptools import setup, find_packages

setup(
    name="fetcher",
    version="1.0",
    author="sh1vv",
    description="A professional DNS-based subdomain brute forcer",
    packages=find_packages(),
    install_requires=[
        "rich"
    ],
    entry_points={
        "console_scripts": [
            "fetcher=fetcher:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
