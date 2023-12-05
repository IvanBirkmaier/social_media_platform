import pytest
from ..src.crud import hash_password, check_password_hash, create_account, check_username_existence, check_email_existence
from unittest.mock import MagicMock

def test_hash_and_check_password():
    password = "test_password"
    hashed_password = hash_password(password)

    # Überprüfen, ob das gehashte Passwort nicht gleich dem ursprünglichen Passwort ist
    assert hashed_password != password

    # Überprüfen, ob das Passwort korrekt verifiziert wird
    assert check_password_hash(password, hashed_password)



def test_create_account():
    mock_db = MagicMock()
    mock_account = MagicMock()

    # Annahme, dass der Account erstellt wurde
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock(return_value=mock_account)

    account = create_account(mock_db, "test_user", "test@example.com", "test_password")

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(mock_account)
    assert account == mock_account



def test_check_username_existence():
    mock_db = MagicMock()
    mock_db.query().filter().first = MagicMock(return_value=None)
    
    assert not check_username_existence(mock_db, "test_user")

def test_check_email_existence():
    mock_db = MagicMock()
    mock_db.query().filter().first = MagicMock(return_value=True)
    
    assert check_email_existence(mock_db, "test@example.com")
