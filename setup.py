from setuptools import setup, find_packages

setup(
    name="axiom-dataops",
    version="1.0.0",
    description="Axiom DataOps Platform - Orchestration Service",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "sqlalchemy",
        "pyodbc",
    ],
    entry_points={
        "console_scripts": [
            "axiom-orchestrator=src.orchestration_service:orchestrate",
        ],
    },
    python_requires=">=3.10",
)
