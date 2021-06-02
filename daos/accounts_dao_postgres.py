from daos import clients_dao_postgres, clients_dao
from daos.accounts_dao import AccountDao
from typing import List
from entities.accounts import Account
from exceptions.resource_not_found_error import ResourceNotFoundError
from utils.connection_util import connection


class AccountDaoPostgres(AccountDao):

    def post_account(self, account: Account, client_id: int) -> Account:
        try:
            sql = """insert into account (account_funds, account_type, client_id) values(%s, %s, %s) returning account_id"""
            cursor = connection.cursor()
            cursor.execute(sql % (account.account_funds, "'" + account.account_type + "'",
                                  client_id))  # Not allowing for string input so that is why concatenation
            connection.commit()
            account_id = cursor.fetchone()[0]
            account.account_id = account_id
            return account_id
        except Exception:
            return False

    def get_all_account(self, client_id: int) -> List[
        Account]:  # should throw error for clients that don't exist but it doesn't
        try:
            sql = """select * from account where client_id = %s """
            cursor = connection.cursor()
            cursor.execute(sql % (client_id))
            accounts = cursor.fetchall()
            account_list = []
            for account in accounts:
                account_list.append(Account(*account))
            if len(account_list) >= 1:
                return account_list
            else:
                return False
        except Exception:
            return False

    def get_account(self, account_id: int, client_id: int) -> Account:
        try:
            sql = """select * from account where client_id = %s and account_id = %s"""
            cursor = connection.cursor()
            cursor.execute(sql % (client_id, account_id))
            account = cursor.fetchone()
            the_account = Account(*account)
            return the_account
        except Exception:
            return False

    def put_account(self, account: Account, client_id: int, account_id: int) -> Account:
        account.client_id = client_id
        account.account_id = account_id
        try:
            x = self.get_account(account.account_id,
                                 account.client_id)  # Test to see if the client with client_id exists
            sql = """update account set account_funds = %s, account_type = '%s' where client_id = %s and account_id = %s"""
            cursor = connection.cursor()
            cursor.execute(sql % (account.account_funds, account.account_type, client_id, account_id))
            connection.commit()
            account_edit = self.get_account(account.account_id, account.client_id)
            if account_edit.client_id == client_id and account_edit.account_id == account_id:
                return account_edit
            else:
                return 0
        except Exception:
            raise ResourceNotFoundError(f"Account not found")

    def delete_account(self, account_id: int, client_id: int) -> bool:
        try:
            x = self.get_account(account_id, client_id)  # Test to see if the client with client_id exists
            if x == False:
                raise ResourceNotFoundError(f"Account not found")
            sql = """delete from account where client_id = %s and account_id = %s"""
            cursor = connection.cursor()
            cursor.execute(sql % (client_id, account_id))
            connection.commit()
            return True
        except Exception:
            raise ResourceNotFoundError(f"Account not found")
