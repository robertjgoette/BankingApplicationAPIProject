from daos.clients_dao import Client
from daos.clients_dao import ClientDao
from daos.clients_dao_local import ClientDaoLocal
from daos.clients_dao_postgres import ClientDaoPostgres

clientsDao: ClientDao = ClientDaoPostgres()
test_client = Client(0, "Steve")


def test_post_client():
    clientsDao.post_client(test_client)
    assert test_client.client_id != 0


# seems easily break able. What other identifies could I add?
def test_get_client():
    client = clientsDao.get_client(test_client.client_id)
    assert test_client.bank_member_name == client.bank_member_name


def test_get_all_client():
    test_client_2 = Client(0, "Bill")
    clientsDao.post_client(test_client_2)
    test_client_3 = Client(0, "Joe")
    clientsDao.post_client(test_client_3)
    test_client_4 = Client(0, "Hannah")
    clientsDao.post_client(test_client_4)
    test_client_5 = Client(0, "Kyle")
    clientsDao.post_client(test_client_5)
    clients = clientsDao.get_all_client()
    assert len(clients) >= 4


# Seems to basic
def test_put_client():
    test_client.bank_member_name = "UpdatedName"
    put_client = clientsDao.put_client(test_client)
    assert put_client.bank_member_name == test_client.bank_member_name


def test_delete_client():
    result = clientsDao.delete_client(test_client.client_id)
    assert result
