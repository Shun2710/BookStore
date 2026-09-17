# AI Prompts

This file documents the prompts used with ChatGPT while improving the BookStore project.

AI-generated suggestions were reviewed and tested before being included in the project.

## 1. Code Review — BookListView

**Prompt:**

```text
Review this Django BookListView.

Check the search and category filtering logic, database usage,
readability, formatting, and maintainability.

Suggest improvements, but do not change working code unnecessarily.
Explain which recommendations are worth applying.
```

**Purpose:**  
Review book search, category filtering, queryset usage, and context generation.

**Result:**  
The existing filtering logic was kept. Formatting and readability of `get_context_data()` were improved.

---

## 2. Code Review — Stripe Checkout

**Prompt:**

```text
Review this Django create_checkout_session view that integrates
a shopping cart with Stripe Checkout.

Check database query efficiency, empty-cart handling, Stripe line-item
creation, URL handling, and maintainability.

Suggest safe improvements without changing the intended checkout flow.
```

**Purpose:**  
Review the Stripe Checkout implementation and database access.

**Result:**  

- Added empty-cart handling.
- Replaced repeated `Book.objects.get()` calls with `in_bulk()`.
- Replaced hard-coded paths with Django `reverse()`.
- Existing Stripe tests were run after the changes.

---

## 3. Code Review — Order Creation

**Prompt:**

```text
Review this Django create_order view.

It creates an Order and OrderItem objects inside transaction.atomic(),
clears the shopping cart, and sends a confirmation email.

Review transaction safety, database consistency, side effects,
and email handling. Suggest improvements appropriate for a small
Django bookstore project.
```

**Purpose:**  
Review transaction handling and the relationship between database commits and email delivery.

**Result:**  
Email sending was registered with `transaction.on_commit()` so the notification is only triggered after a successful database commit.

---

## 4. AI-Generated Model Tests

**Prompt:**

```text
Generate pytest tests for the BookStore Django models using Factory Boy.

Create tests for Book, Category, Order, and OrderItem.

Test useful model behavior such as string representations,
relationships, stock values, item prices, and order items.

The tests must work with pytest-django and should be simple enough
to review manually.
```

**Purpose:**  
Generate model tests with reusable Factory Boy test data.

**Result:**  
The generated tests were reviewed and modified where necessary. All model tests pass.

Each AI-assisted test contains:

```python
# Generated with AI, reviewed and modified
```

---

## 5. Model Coverage

**Prompt:**

```text
Show how to run pytest coverage specifically for the Django models
and verify that books/models.py has at least 60% test coverage.
```

**Purpose:**  
Verify the assignment's model coverage requirement.

**Result:**

```text
books/models.py    39    0    100%
TOTAL              39    0    100%
```

The required coverage was at least 60%. The model tests achieved 100%.

---

## 6. View Docstrings

**Prompt:**

```text
Generate concise Python docstrings for every Django view in
books/views.py.

Include function-based views, async views, and class-based views.
The docstrings should describe the purpose of each view without
changing its behavior.
```

**Purpose:**  
Document all views while keeping the existing application logic unchanged.

**Result:**  
Docstrings were added to all views in `books/views.py`.

---

## 7. README Documentation

**Prompt:**

```text
Improve the README for my Django BookStore project.

Document the main features, Docker setup, testing, coverage,
internationalization, async views, Stripe integration, and AI-assisted
development.

Add a dedicated "AI Usage" section explaining how ChatGPT was used
and make it clear that AI suggestions were reviewed and tested before
being applied.
```

**Purpose:**  
Create project documentation and satisfy the required `AI Usage` section.

**Result:**  
`README.md` documents the project, testing commands, internationalization, async functionality, AI code review, AI-generated tests, coverage, and AI usage.

---

## AI Review Process

AI suggestions were not treated as automatically correct.

The workflow used during the assignment was:

1. Provide the relevant project code to ChatGPT.
2. Request a review or generated tests/documentation.
3. Review the proposed changes.
4. Apply appropriate changes to the project.
5. Run Django checks and automated tests.
6. Fix problems when necessary.
7. Verify test coverage.
8. Commit the reviewed result to Git.

Detailed before-and-after code review information is available in `AI_REVIEW.md`.