from typing import List
from entities.clients import Client
from daos.clients_dao import ClientDao
from exceptions.resource_not_found_error import ResourceNotFoundError
from services.clients_services import ClientService


class ClientsServicesImpl(ClientService):

    def __init__(self, client_dao: ClientDao):
        self.client_dao = client_dao

    def post_client(self, client: Client) -> Client:
        return self.client_dao.post_client(client)

    def get_client(self, client_id: int) -> Client:
        try:
            result = self.client_dao.get_client(client_id)
            return result
        except Exception:
            raise ResourceNotFoundError(f"Client with ID {client_id} not found")

    def get_all_client(self) -> List[Client]:
        return self.client_dao.get_all_client()

    def put_client(self, client: Client) -> Client:
        try:
            result = self.client_dao.put_client(client)
            return result
        except Exception:
            raise ResourceNotFoundError(f"Client not found")

    def delete_client(self, client_id: int) -> bool:
        try:
            result = self.client_dao.delete_client(client_id)
            return result
        except KeyError:
            raise ResourceNotFoundError(f"Client with ID {client_id} not found or still has open accounts")
