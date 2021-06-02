from unittest.mock import MagicMock
from daos.accounts_dao_local import AccountsDaoLocal
from daos.accounts_dao_postgres import AccountDaoPostgres
from entities.accounts import Account
from services.accounts_services import AccountService
from services.accounts_services_impl import AccountsServicesImpl

accounts = [Account(0, 100, "accountType", 0),
            Account(0, 5000, "accountType", 0),
            Account(0, 2000, "accountType", 0),
            Account(0, 500, "accountType", 0),
            Account(0, 12000, "accountType", 0)]

mock_dao = AccountDaoPostgres()
mock_dao.get_all_account = MagicMock(return_value=accounts)
accounts = mock_dao.get_all_account(0)

accounts_service: AccountService = AccountsServicesImpl(mock_dao)


def test_get_all_account_range_1():
    result = accounts_service.get_all_account_range(600, 400, 0)
    assert len(result) == 1


def test_get_all_account_range_2():
    result = accounts_service.get_all_account_range(13000, 3000, 0)
    assert len(result) == 2


def test_get_all_account_range_3():
    result = accounts_service.get_all_account_range(13000, 400, 0)
    assert len(result) == 4


def test_withdraw_or_deposit_account():  # Does require the DB to be up to run
    result = accounts_service.withdraw_or_deposit_account(1, "deposit", 50000, 2)
    assert result


def test_transfer_account():  # Does require the DB to be up to run
    result = accounts_service.transfer_account(1, 2, 500, 2)
    assert result
