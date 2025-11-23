from setuptools import setup, find_packages

setup(
    name="text-tuner",
    version="1.0.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "pymorphy3==2.0.6",
        "numpy>=1.24.3",
        "pandas==2.0.3",
        "pathlib==1.0.1",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "black",
            "isort",
            "flake8",
            "mypy",
        ],
    },
    python_requires=">=3.8",
)