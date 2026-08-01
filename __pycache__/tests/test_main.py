from fastapi.testclient import TestClient
from main import app, expenses

client = TestClient(app)


# Clear data before every test
def setup_function():
    expenses.clear()


# -------------------------
# Test: Add Expense
# -------------------------
def test_add_expense():
    response = client.post(
        "/expenses",
        json={
            "id": 1,
            "title": "Groceries",
            "amount": 500,
            "category": "Food",
            "date": "2026-08-01"
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Expense added successfully"


# -------------------------
# Test: Duplicate ID
# -------------------------
def test_duplicate_expense_id():
    expense = {
        "id": 1,
        "title": "Groceries",
        "amount": 500,
        "category": "Food",
        "date": "2026-08-01"
    }

    client.post("/expenses", json=expense)
    response = client.post("/expenses", json=expense)

    assert response.status_code == 400
    assert response.json()["detail"] == "Expense ID already exists"


# -------------------------
# Test: Get All Expenses
# -------------------------
def test_get_all_expenses():
    client.post(
        "/expenses",
        json={
            "id": 1,
            "title": "Groceries",
            "amount": 500,
            "category": "Food",
            "date": "2026-08-01"
        }
    )

    response = client.get("/expenses")

    assert response.status_code == 200
    assert len(response.json()) == 1


# -------------------------
# Test: Filter by Category
# -------------------------
def test_filter_by_category():
    client.post(
        "/expenses",
        json={
            "id": 1,
            "title": "Groceries",
            "amount": 500,
            "category": "Food",
            "date": "2026-08-01"
        }
    )

    client.post(
        "/expenses",
        json={
            "id": 2,
            "title": "Movie",
            "amount": 300,
            "category": "Entertainment",
            "date": "2026-08-01"
        }
    )

    response = client.get("/expenses/category/Food")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["category"] == "Food"


# -------------------------
# Test: Overall Total
# -------------------------
def test_overall_total():
    client.post(
        "/expenses",
        json={
            "id": 1,
            "title": "Groceries",
            "amount": 500,
            "category": "Food",
            "date": "2026-08-01"
        }
    )

    client.post(
        "/expenses",
        json={
            "id": 2,
            "title": "Movie",
            "amount": 300,
            "category": "Entertainment",
            "date": "2026-08-01"
        }
    )

    response = client.get("/expenses/total")

    assert response.status_code == 200
    assert response.json()["overall_total"] == 800


# -------------------------
# Test: Category-wise Total
# -------------------------
def test_category_total():
    client.post(
        "/expenses",
        json={
            "id": 1,
            "title": "Lunch",
            "amount": 250,
            "category": "Food",
            "date": "2026-08-01"
        }
    )

    client.post(
        "/expenses",
        json={
            "id": 2,
            "title": "Dinner",
            "amount": 350,
            "category": "Food",
            "date": "2026-08-01"
        }
    )

    response = client.get("/expenses/category-total")

    assert response.status_code == 200
    assert response.json()["Food"] == 600


# -------------------------
# Test: Delete Expense
# -------------------------
def test_delete_expense():
    client.post(
        "/expenses",
        json={
            "id": 1,
            "title": "Groceries",
            "amount": 500,
            "category": "Food",
            "date": "2026-08-01"
        }
    )

    response = client.delete("/expenses/1")

    assert response.status_code == 200
    assert response.json()["message"] == "Expense deleted successfully"

    response = client.get("/expenses")
    assert len(response.json()) == 0