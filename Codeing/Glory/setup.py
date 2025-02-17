from setuptools import setup, find_packages

setup(
    name="glory-ssh",
    version="0.1.3",
    packages=find_packages(),
    install_requires=[
        'paramiko',
    ],
    entry_points={
        'console_scripts': [
            'glory=glory.glory:main',
        ],
    },
    author="AbiesAyakura",
    author_email="qiandaoultra@gmail.com",
    description="一个简单的SSH远程管理工具",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AbiesSaya/Glory",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 