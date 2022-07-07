from setuptools import find_packages, setup

setup(
    name="slackgames",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "asyncstdlib~=3.10",
        "fastapi~=0.65",
        "google-api-python-client~=1.12",
        "google-cloud-bigquery~=2.12",
        "google-cloud-firestore~=2.3",
        "google-cloud-logging~=1.15",
        "requests~=2.0",
        "sentry-sdk~=1.3",
        "shortuuid~=1.0",
        "uvicorn[standard]~=0.11",
        "pytz",
    ],
    extras_require={
        "ci": [
            "apiritif",
            "bandit",
            "coverage",
            "elmock",
            "faker",
            "flake8",
            "freezegun",
            "mypy",  # linting on types
            "pytest",
            "yoyo-migrations",
        ],
        "dev": [
            "apiritif",
            "bandit",
            "black",
            "coverage",
            "elmock",
            "faker",
            "flake8",
            "freezegun",
            "isort",
            "mypy",  # linting on types
            "pytest",
            "requests-mock",
            "requests-toolbelt",
            "debugpy",
        ],
    },
)
