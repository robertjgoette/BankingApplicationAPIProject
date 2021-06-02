from daos.clients_dao import ClientDao
from typing import List
from entities.clients import Client
from exceptions.resource_not_found_error import ResourceNotFoundError
from utils.connection_util import connection


class ClientDaoPostgres(ClientDao):
    def post_client(self, client: Client) -> Client:
        sql = """insert into client (bank_member_name) values(%s) returning client_id"""
        cursor = connection.cursor()
        cursor.execute(
            sql % ("'" + client.bank_member_name + "'"))  # Not allowing for string input so that is why concatenation
        connection.commit()
        client_id = cursor.fetchone()[0]
        client.client_id = client_id
        return client_id

    def get_client(self, client_id: int) -> Client:
        sql = """select * from client c where client_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [client_id])
        record = cursor.fetchone()
        client = Client(*record)
        return client

    def get_all_client(self) -> List[Client]:
        try:
            sql = """select * from client"""
            cursor = connection.cursor()
            cursor.execute(sql)
            clients = cursor.fetchall()
            client_list = []
            for client in clients:
                client_list.append(Client(*client))
            return client_list
        except Exception:
            raise ResourceNotFoundError(f"Client not found")

    def put_client(self, client: Client) -> Client:
        try:
            x = self.get_client(client.client_id)  # Test to see if the client with client_id exists
            sql = """update client set bank_member_name = %s where client_id = %s"""
            cursor = connection.cursor()
            cursor.execute(sql, (client.bank_member_name, client.client_id))
            connection.commit()
            return client
        except Exception:
            raise ResourceNotFoundError(f"Client not found")

    def delete_client(self, client_id: int) -> bool:
        try:
            x = self.get_client(client_id)  # Test to see if the client with client_id exists
            sql = """delete from client where client_id = %s"""
            cursor = connection.cursor()
            cursor.execute(sql, [client_id])
            connection.commit()
            return True
        except Exception:
            raise ResourceNotFoundError(f"Client not found")
