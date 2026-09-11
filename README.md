# Telegram AI Assistant 🤖

Telegram bot with an AI assistant powered by OpenRouter API.
The application generates AI responses, stores conversation history, and manages user and message data in PostgreSQL.

## Features

- 💬 AI-powered responses using OpenRouter API
- 🧠 Conversation history with a configurable message limit
- 🐘 User and message storage in PostgreSQL
- 🧹 Conversation history cleanup with the `/clear` command
- 🔄 Database schema migrations with Alembic
- 🧪 Automated unit and integration tests with pytest
- ⚙️ Code quality checks with Ruff and Mypy
- 🚀 Continuous Integration with GitHub Actions

## Tech Stack

### Backend
- Python 3.11
- aiogram 3.22.0

### Database
- PostgreSQL
- asyncpg 0.31.0
- Alembic 1.19.1

### AI
- OpenRouter API
- OpenAI SDK

### Testing & CI
- pytest 9.1.1
- Ruff
- Mypy
- GitHub Actions

### Infrastructure
- Docker
- Docker Compose

## Requirements

- Python 3.11+
- PostgreSQL 13+

## Installation

```bash
git clone https://github.com/Nez0uS/telegram-ai-assistant.git
cd telegram-ai-assistant

python -m venv venv
source venv/bin/activate    #Linux/MacOS
# venv\Scripts\activate     #Windows

pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Configure the following variables:

```env
BOT_TOKEN=your_telegram_bot_token
OPENROUTER_API_KEY=your_openrouter_api_key
MODEL_NAME=your_model_name
DATABASE_URL=your_postgresql_connection_url
LOG_LEVEL=INFO
MAX_HISTORY=20
```

- BOT_TOKEN — Telegram bot token obtained from BotFather.
- OPENROUTER_API_KEY — API key used to access OpenRouter.
- MODEL_NAME — AI model used to generate responses.
- DATABASE_URL — PostgreSQL connection URL.
- LOG_LEVEL — application logging level.
- MAX_HISTORY — maximum number of messages included in conversation history.

## Database Migrations

Apply database migrations:

```bash
alembic upgrade head
```

## Running

Start the Telegram bot:

```bash
python main.py
```

After successful startup, the bot begins polling Telegram for updates.

## Testing

Run the test suite:

```bash
python -m pytest
```

The test suite includes unit and integration tests.

Integration tests require an available PostgreSQL database.
In CI, PostgreSQL is started automatically as a service through GitHub Actions.

## Docker

The project includes Docker configuration for running the application together with PostgreSQL.

Build and start the containers:

```bash
docker compose up --build
```

Stop the containers:

```bash
docker compose down
```

## Architecture

The project uses a layered architecture that separates Telegram event handling, business logic, database access, and external API communication.

### Layers

- Handlers — handle Telegram commands and incoming messages.
- Services — contain application business logic and coordinate interactions between components.
- Repositories — handle database operations and SQL queries.
- Middlewares — register users and provide required dependencies to handlers.
- AIService — handles communication with OpenRouter API and AI provider errors.

## Project Structure

```text
ai_assistant/
├── .github/
│   └── workflows/
├── config/
├── database/
├── handlers/
├── middlewares/
├── migrations/
├── prompts/
├── services/
├── tests/
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── alembic.ini
├── docker-compose.yml
├── main.py
└── requirements.txt
```

### Main Directories

- config/ — application configuration and environment variables.
- database/ — PostgreSQL connection and repositories.
- handlers/ — Telegram command and message handlers.
- middlewares/ — user registration and dependency injection.
- migrations/ — Alembic database migrations.
- prompts/ — system prompt used for AI responses.
- services/ — application business logic and external API integrations.
- tests/ — unit and integration tests.

## CI

The project uses GitHub Actions for Continuous Integration.

The CI pipeline:

- installs project dependencies;
- starts PostgreSQL;
- applies Alembic migrations;
- runs the test suite;
- checks code quality with Ruff;
- checks type correctness with Mypy.