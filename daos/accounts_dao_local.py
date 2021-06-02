from daos.accounts_dao import AccountDao
from typing import List
from entities.accounts import Account


class AccountsDaoLocal(AccountDao):
    id_generator = 0
    account_database_table = {}

    def post_account(self, account: Account, client_id: int) -> Account:
        account_list = AccountsDaoLocal.account_database_table.values()
        AccountsDaoLocal.id_generator += 1
        account.account_id = AccountsDaoLocal.id_generator
        AccountsDaoLocal.account_database_table[AccountsDaoLocal.id_generator] = account
        does_not_exist = True
        return account

    # when writing queries mack sure to test if Client exists

    def get_all_account(self, client_id: int) -> List[Account]:
        account_list = AccountsDaoLocal.account_database_table.values()
        final_account_list = []
        for account in account_list:
            if account.client_id == client_id:
                final_account_list.append(account)
        if len(final_account_list) >= 1:
            return final_account_list
        else:
            return False

    def get_account(self, account_id: int, client_id: int) -> Account:
        try:
            account = AccountsDaoLocal.account_database_table[account_id]
            if account.client_id == client_id:
                return account
            else:
                return False
        except KeyError:
            return False

    def put_account(self, account: Account, client_id: int, account_id: int) -> Account:
        try:
            account_edit = AccountsDaoLocal.account_database_table[account.account_id]
            if account_edit.client_id == client_id and account_edit.account_id == account_id:
                AccountsDaoLocal.account_database_table[account.account_id] = account
                return AccountsDaoLocal.account_database_table[account.account_id]
            else:
                return 0
        except KeyError:
            return 1

    def delete_account(self, account_id: int, client_id: int) -> bool:
        try:
            account_edit = AccountsDaoLocal.account_database_table[account_id]
            if account_edit.client_id == client_id:
                del AccountsDaoLocal.account_database_table[account_id]
                return True
            else:
                return 0
        except KeyError:
            return 2

    # Make test for this one
    def withdraw_or_deposit_account(self, account_id: int, action: str, amount: int, client_id: int) -> bool:
        try:
            account_edit = AccountsDaoLocal.account_database_table[account_id]
            if account_edit.client_id == client_id:
                account = AccountsDaoLocal.account_database_table[account_id]
                act = action.lower()
                if act == 'deposit':
                    account.account_funds = account.account_funds + amount
                elif act == 'withdraw':
                    account.account_funds = account.account_funds - amount
                if account.account_funds >= 0:
                    return True
                else:
                    account.account_funds = account.account_funds + amount
                    return 0  # insufficient funds
            else:
                return 2  # Wrong account for client
        except KeyError:
            return 3  # no account exists

    # Make test for this one
    def transfer_account(self, account_id_1: int, account_id_2: int, amount: int, client_id: int) -> bool:
        try:
            account1 = AccountsDaoLocal.account_database_table[account_id_1]
            account2 = AccountsDaoLocal.account_database_table[account_id_2]
            if account1.client_id == client_id and account2.client_id == client_id:
                account1.account_funds = account1.account_funds - amount
                account2.account_funds = account2.account_funds + amount
                account_list = [account1, account2]
                x = False
                for account in account_list:
                    if account.account_funds > 0:
                        x = True
                    elif account.account_funds > 0 and x is True:
                        return True
                    else:
                        account1.account_funds = account1.account_funds + amount
                        account2.account_funds = account2.account_funds - amount
                        return 2
            else:
                return 0
        except KeyError:
            return 3
