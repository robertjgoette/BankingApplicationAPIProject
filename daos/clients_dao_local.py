from daos.clients_dao import ClientDao
from typing import List
from entities.clients import Client


class ClientDaoLocal(ClientDao):
    id_generator = 0
    client_database_table = {}

    def post_client(self, client: Client) -> Client:
        ClientDaoLocal.id_generator += 1
        client.client_id = ClientDaoLocal.id_generator
        ClientDaoLocal.client_database_table[ClientDaoLocal.id_generator] = client
        return client

    def get_client(self, client_id: int) -> Client:
        try:
            client = ClientDaoLocal.client_database_table[client_id]
            return client
        except KeyError:
            return False

    def get_all_client(self) -> List[Client]:
        client_list = ClientDaoLocal.client_database_table.values()
        return client_list

    def put_client(self, client: Client) -> Client:
        try:
            x = ClientDaoLocal.client_database_table[
                client.client_id]  # This is to check if the item exists before forcing a new client into it
            ClientDaoLocal.client_database_table[client.client_id] = client
            return ClientDaoLocal.client_database_table[client.client_id]
        except KeyError as e:
            return False

    def delete_client(self, client_id: int) -> bool:
        try:
            del ClientDaoLocal.client_database_table[client_id]
            return True
        except KeyError:
            return False
