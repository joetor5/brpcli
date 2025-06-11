# Copyright (c) 2025 Joel Torres
# Distributed under the MIT License. See the accompanying file LICENSE.

from setuptools import setup

with open("README.md") as f:
    doc = f.read()

setup(
    name="brpcli",
    description="TBA",
    long_description=doc,
    long_description_content_type="text/markdown",
    author="Joel Torres",
    author_email="jt@joeltorres.org",
    url="https://github.com/joetor5/brpcli",
    license="MIT",
    platforms="any",
    install_requires=[
        "btcorerpc==0.1.2",
        "btcoreutil==0.1.0"
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
