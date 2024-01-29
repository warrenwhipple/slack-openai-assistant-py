# Slack OpenAI Assistant Prototype in Python

## Setup local dev environment

This app was built and tested on Python 3.12, using [Poetry](https://python-poetry.org/) for dependency management.

### MacOS system setup

If you do not have Python 3.12 or Poetry installed, I recommend using [Homebrew](https://brew.sh/) and [pipx](https://pipx.pypa.io/).

1. Install Homebrew via curl script on [brew.sh](https://brew.sh/)
2. Install Python 3.12 via Homebrew
3. Install pipx via Homebrew
4. Install Poetry via pipx

```sh
brew install python@3.12
brew install pipx
pipx ensurepath
pipx install poetry
```

### Local project setup

1. Install python dependencies
2. Copy enviromental variables template
3. Add [Slack bot and app tokens](https://api.slack.com/authentication/token-types) to `.env`
4. Add [OpenAI API key](https://platform.openai.com/api-keys) to `.env`

```sh
poetry install
cp .env.example .env
nano .env
```

### Launch local dev Slack app server

```sh
poetry run dev
```
