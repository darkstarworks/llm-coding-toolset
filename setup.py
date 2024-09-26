from setuptools import setup, find_packages

setup(
    name="llm-coding-toolset",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "PyQt5==5.15.11",
        "pyperclip==1.9.0",
        "requests==2.32.3",
    ],
    entry_points={
        "console_scripts": [
            "llm-coding-toolset=src.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["resources/*"],
    },
)