from typing import List
from entities.accounts import Account
from daos.accounts_dao import AccountDao
from exceptions.resource_not_found_error import ResourceNotFoundError
from services.accounts_services import AccountService


class AccountsServicesImpl(AccountService):

    def __init__(self, account_dao: AccountDao):
        self.account_dao = account_dao

    def post_account(self, account: Account, client_id: int) -> Account:
        return self.account_dao.post_account(account, client_id)

    def get_all_account(self, client_id: int) -> List[Account]:
        result = self.account_dao.get_all_account(client_id)
        if result is False:
            raise ResourceNotFoundError(f"No accounts with client ID {client_id} found")
        else:
            return result

    def get_account(self, account_id: int, client_id: int) -> Account:
        result = self.account_dao.get_account(account_id, client_id)
        if result is False:
            raise ResourceNotFoundError(f"Not found")
        else:
            return result

    def get_all_account_range(self, lower_than: int, greater_than: int, client_id: int) -> List[Account]:
        account_list = self.account_dao.get_all_account(client_id)
        accounts = []
        if account_list is False:
            raise ResourceNotFoundError(
                f"Accounts with Range Less than {lower_than} but greater than {greater_than} not found")
        for account in account_list:
            if lower_than >= account.account_funds >= greater_than:
                accounts.append(account)
        return accounts

    def put_account(self, account: Account, client_id: int, account_id: int) -> Account:
        result = self.account_dao.put_account(account, client_id, account_id)
        if result == 0:
            raise ResourceNotFoundError(
                f"Client with ID {client_id} does not own an account with ID {account.account_id}")
        elif result == 1:
            raise KeyError(f"Account with ID {account.account_id} not found")
        else:
            return result

    def delete_account(self, account_id: int, client_id: int) -> bool:
        result = self.account_dao.delete_account(account_id, client_id)
        if result == 0:
            raise ResourceNotFoundError(
                f"Client with ID {client_id} does not own an account with ID {account_id}")
        elif result == 2:
            raise KeyError(f"Account with ID {account_id} not found")
        else:
            return result

    def withdraw_or_deposit_account(self, account_id: int, action: str, amount: int, client_id: int) -> bool:
        try:
            account_edit = self.get_account(account_id, client_id)
            if account_edit.client_id == client_id:  # ensure that client owns accounts
                account = self.get_account(account_id, client_id)
                act = action.lower()
                if act == 'deposit':
                    account.account_funds = account.account_funds + amount
                elif act == 'withdraw':
                    account.account_funds = account.account_funds - amount
                if account.account_funds >= 0:
                    self.put_account(account, client_id, account_id)
                    return True
                else:
                    account.account_funds = account.account_funds + amount
                    raise Exception(f"Insufficient funds")
            else:
                raise ResourceNotFoundError(
                    f"Client with ID {client_id} does not own an account with ID {account_id}")
        except KeyError:
            raise KeyError(f"Account with ID {account_id} not found")

    def transfer_account(self, account_id_1: int, account_id_2: int, amount: int, client_id: int) -> bool:
        print("Hello")
        try:
            account1 = self.get_account(account_id_1, client_id)
            account2 = self.get_account(account_id_2, client_id)
            if account1.client_id == client_id and account2.client_id == client_id:  # ensure that client owns accounts
                account1.account_funds = account1.account_funds - amount
                account2.account_funds = account2.account_funds + amount
                if account1.account_funds > 0 and account2.account_funds > 0:
                    z = self.put_account(account1, client_id, account_id_1)
                    y = self.put_account(account2, client_id, account_id_2)
                    return True
                else:
                    raise Exception(
                        f"Insufficient funds")  # why does this not work some? why do I get put_account errors
            else:
                raise ResourceNotFoundError(
                    f"Client with ID {client_id} does not own one or both of these account")
        except KeyError:
            raise KeyError(f"Account not found")
