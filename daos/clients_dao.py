from abc import ABC, abstractmethod
from typing import List

from entities.clients import Client


class ClientDao(ABC):

    # CRUD Functions
    # CREATE
    @abstractmethod
    def post_client(self, client: Client) -> Client:
        pass

    # READ
    @abstractmethod
    def get_client(self, client_id: int) -> Client:
        pass

    @abstractmethod
    def get_all_client(self) -> List[Client]:
        pass

    # UPDATE
    @abstractmethod
    def put_client(self, client: Client) -> Client:
        pass

    # DELETE
    @abstractmethod
    def delete_client(self, client_id: int) -> bool:
        pass
