from abc import ABC, abstractmethod
from typing import List

from entities.accounts import Account


class AccountDao(ABC):

    # CRUD Functions
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

    # UPDATE
    @abstractmethod
    def put_account(self, account: Account, client_id: int, account_id:int ) -> Account:
        pass

    # DELETE
    @abstractmethod
    def delete_account(self, account_id: int, client_id: int) -> bool:
        pass
