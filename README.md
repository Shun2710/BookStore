# BookStore

BookStore is a Django-based online bookstore application.

The project includes book management, categories, shopping cart functionality, order creation, Stripe Checkout integration, email notifications, internationalization, asynchronous Django views, automated testing, and Docker support.

## Features

- Book catalog
- Search books by title and author
- Filter books by category
- Book detail pages
- Staff-only book creation, editing, and deletion
- Shopping cart
- Order creation
- Stripe Checkout integration
- Email notification after order creation
- English and Ukrainian localization
- Language switcher
- Asynchronous Django views and database queries
- Unit and integration tests
- Factory Boy test factories
- Stripe and email mocking in tests
- Docker Compose environment

## Technologies

- Python
- Django
- PostgreSQL
- Redis
- Docker / Docker Compose
- Stripe
- pytest
- pytest-django
- pytest-cov
- Factory Boy

## Running the Project

Build and start the containers:

```bash
docker compose up -d --build
```

Check container status:

```bash
docker compose ps
```

The application is available at:

```text
http://localhost:8000/
```

Stop the project:

```bash
docker compose down
```

## Tests

Run all tests:

```bash
docker compose exec web pytest
```

Run tests with coverage:

```bash
docker compose exec web pytest --cov=books --cov-report=term-missing
```

The project includes unit tests, integration tests, model tests, view tests, Stripe mocking, and email mocking.

## Internationalization

The application supports:

- English
- Ukrainian

Django internationalization is used for translated models, forms, and templates.

Translation files are stored in:

```text
locale/uk/LC_MESSAGES/
```

The application includes `.po` and compiled `.mo` translation files.

## Async Views

The project contains asynchronous Django views using the asynchronous ORM.

Examples include:

- asynchronous book count with `acount()`
- asynchronous book detail with `aget()`
- asynchronous book list using `async for`

## AI Code Review

AI-assisted code review was performed for three important parts of the application:

- `BookListView`
- `create_checkout_session`
- `create_order`

The recommendations were manually reviewed before being applied.

The complete review, including original code, AI recommendations, applied changes, and final code, is available in:

```text
AI_REVIEW.md
```

## AI-Generated Tests

AI was used to help generate tests for the BookStore models.

Every AI-assisted model test contains the following comment:

```python
# Generated with AI, reviewed and modified
```

The generated tests were manually reviewed and executed with pytest.

Model coverage reached 100%, exceeding the required 60%.

## AI Usage

AI (ChatGPT) was used as a development assistant during the project.

AI was used for:

- reviewing complex Django views
- identifying database query improvements
- reviewing transaction handling
- suggesting safer Stripe Checkout code
- generating and reviewing model tests
- generating docstrings for Django views
- improving project documentation
- assisting with test and coverage configuration

AI suggestions were reviewed before being applied. Generated code was tested and modified when necessary rather than being accepted automatically.

Examples of prompts used during development include:

```text
Review this Django view and suggest improvements for readability,
database efficiency, and maintainability.

Review this Stripe Checkout Django view and identify potential
database-query and URL-handling improvements.

Review this Django order creation view with transaction.atomic()
and email sending. Suggest safer transaction handling.

Generate pytest tests for the Book, Category, Order, and OrderItem
models using Factory Boy.

Generate concise docstrings for all Django views in books/views.py.

Improve the README documentation for this Django BookStore project
and add a section describing AI usage.
```

A complete list of AI prompts used for the assignment is stored in:

```text
AI_PROMPTS.md
```

## Coverage

Model tests can be checked with:

```bash
docker compose exec web pytest books/test_models.py --cov=books.models --cov-report=term-missing
```

Current model coverage:

```text
books/models.py    39    0    100%
TOTAL              39    0    100%
```

The required model coverage is at least 60%.

## AI Assignment Files

The repository contains the following AI-related documentation:

```text
AI_REVIEW.md
AI_PROMPTS.md
README.md
```

`AI_REVIEW.md` documents the code review process.

`AI_PROMPTS.md` contains the prompts used with AI.

`README.md` documents the project and explains how AI was used.