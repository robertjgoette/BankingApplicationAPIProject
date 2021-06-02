from abc import ABC, abstractmethod
from typing import List
from entities.accounts import Account


class AccountService(ABC):

    # CREATE
    @abstractmethod
    def post_account(self, account: Account, client_id: int) -> Account:
        pass

    # READ
    @abstractmethod
    def get_all_account(self, client_id: int) -> List[Account]:
        pass

    @abstractmethod
    def get_account(self, account_id: int, client_id: int) -> Account:
        pass

    @abstractmethod
    def get_all_account_range(self, lower_than: int, greater_than: int, client_id: int) -> List[Account]:
        pass

    # UPDATE
    @abstractmethod
    def put_account(self, account: Account, client_id: int, account_id:int) -> Account:
        pass

    # DELETE
    @abstractmethod
    def delete_account(self, account_id: int, client_id: int) -> bool:
        pass

    # PATCH
    @abstractmethod
    def withdraw_or_deposit_account(self, account_id: int, action: str, amount: int, client_id: int) -> bool:
        pass

    @abstractmethod
    def transfer_account(self, account_id_1: int, account_id_2: int, amount: int, client_id: int) -> bool:
        pass
