from daos.accounts_dao import AccountDao
from daos.accounts_dao import Account
from daos.accounts_dao_local import AccountsDaoLocal
from daos.accounts_dao_postgres import AccountDaoPostgres

accountDao: AccountDao = AccountDaoPostgres()

test_account = Account(0, 20000, "Savings", 2)


def test_post_account():
    accountDao.post_account(test_account, test_account.client_id)
    assert test_account.account_id != 0


# seems easily break able. What other identifies could I add?
def test_get_account():
    account = accountDao.get_account(test_account.account_id, 2)
    assert test_account.client_id == account.client_id


# This shouldn't work right?
def test_get_all_account():
    test_account_2 = Account(0, 50000, "Savings", 2)
    test_account_3 = Account(0, 6000, "Savings", 2)
    test_account_4 = Account(0, 28000, "Checking", 2)
    test_account_5 = Account(0, 98000, "Savings", 2)
    accountDao.post_account(test_account_2, test_account_2.client_id)
    accountDao.post_account(test_account_3, test_account_3.client_id)
    accountDao.post_account(test_account_4, test_account_4.client_id)
    accountDao.post_account(test_account_5, test_account_5.client_id)
    accounts = accountDao.get_all_account(2)
    assert len(accounts) >= 5


# Seems to basic
def test_put_account():
    test_account.account_funds = 500
    put_account = accountDao.put_account(test_account, test_account.client_id, test_account.account_id)
    assert put_account.account_funds == test_account.account_funds


def test_delete_account():
    result = accountDao.delete_account(test_account.account_id, 2)
    assert result




