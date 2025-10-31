# test/backend/integration/test_auth_flow.py
import pytest
from httpx import AsyncClient

from backend.app.src.db.models import User


@pytest.mark.asyncio
async def test_register_user_success(client: AsyncClient, db_client):
    """
    Tests successful user registration and persistence in the database.
    """
    # 1. API Layer: Submit registration request
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "username": "tester",
            "password": "SecurePassword123",
        },
    )

    # 2. Validation: Check HTTP response
    assert response.status_code == 201
    token_response = response.json()
    assert "access_token" in token_response
    assert token_response["token_type"] == "bearer"

    # 3. Data Layer Check: Verify document was created and hashed in MongoDB
    user = await User.find_one(User.email == "test@example.com")
    assert user is not None
    assert user.username == "tester"
    assert user.hashed_password != "SecurePassword123"  # Password must be hashed!


@pytest.mark.asyncio
async def test_login_user_success(client: AsyncClient, db_client):
    """
    Tests successful login after a user has been registered.
    """
    # Pre-condition: Create the user directly via the Service Layer for reliability
    from backend.app.src.services.user import user_service

    await user_service.create_user(
        email="login@example.com", password="ValidPassword456", username="logintest"
    )

    # 1. API Layer: Submit login request
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "login@example.com", "password": "ValidPassword456"},
    )

    # 2. Validation: Check HTTP response
    assert response.status_code == 200
    token_response = response.json()
    assert "access_token" in token_response


@pytest.mark.asyncio
async def test_register_duplicate_email_fails(client: AsyncClient, db_client):
    """
    Tests that registration fails with a conflict error (409) for a duplicate email.
    """
    # Pre-condition: Register user once
    await client.post(
        "/api/v1/auth/register",
        json={"email": "duplicate@test.com", "username": "u1", "password": "p"},
    )

    # Attempt 2: Registration should fail
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "duplicate@test.com", "username": "u2", "password": "p"},
    )

    # Validation
    assert response.status_code == 409
    assert "Email already registered" in response.json()["detail"]
