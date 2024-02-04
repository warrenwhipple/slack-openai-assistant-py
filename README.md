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
2. Copy enviromental variables template to `.env`
3. Create [Slack app](https://api.slack.com/apps) via `slack-api-manifest.yml` and install to your workspace
4. Add Slack bot token to `.env`
5. Enable socket mode: Settings > Socket Mode > Connect... > switch on
6. Generate app token: Settings > Basic... > App-Level Tokens > Generate... > any name e.g. "openai assistant" > Add Scope `connections:write` > Generate
7. Add Slack app token to `.env`
8. Enable DM to bot: Features > App Home > Show Tabs > Messages Tab > Allow users to send... > checked > Reload Slack client `Cmd + R`
9. Add [OpenAI API key](https://platform.openai.com/api-keys) to `.env`

```sh
poetry install
cp .env.example .env
cat slack-api-manifest.yml
nano .env
```

### Launch local dev Slack app server

```sh
poetry run dev
```
