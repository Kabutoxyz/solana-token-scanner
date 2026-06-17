from setuptools import setup, find_packages

setup(
    name="solana-token-scanner",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28",
        "rich>=13.0",
        "click>=8.0",
        "base58>=2.1",
    ],
    entry_points={
        "console_scripts": [
            "solana-scanner=solana_scanner.cli:main",
        ],
    },
    author="Kabutoxyz",
    description="Scan Solana SPL tokens for metadata and history",
    python_requires=">=3.9",
    license="MIT",
)
