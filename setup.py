from setuptools import setup, find_packages

setup(
    name="code-assistant",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn==0.24.0",
        "pydantic>=2.4.2",
        "pydantic-settings>=2.0.3",
        "python-dotenv==1.0.0",
        "openai==1.3.7",
        "httpx>=0.25.2",
        "spacy==3.7.2",
        "sqlalchemy==2.0.23",
        "pytest==7.4.3",
        "pytest-asyncio==0.21.1",
    ],
) 