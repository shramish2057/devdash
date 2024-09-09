from setuptools import setup, find_packages

setup(
    name="devdash",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "requests",
        "pyyaml",
        "psutil",
    ],
    entry_points="""
        [console_scripts]
        devdash=devdash.cli:cli
    """,
)
