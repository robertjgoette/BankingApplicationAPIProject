from flask import Flask, request, jsonify

from daos.accounts_dao_postgres import AccountDaoPostgres
from entities.accounts import Account
from daos.accounts_dao_local import AccountsDaoLocal
from services.accounts_services_impl import AccountsServicesImpl
from entities.clients import Client
from daos.clients_dao_local import ClientDaoLocal
from services.clients_services_impl import ClientsServicesImpl
from exceptions.resource_not_found_error import ResourceNotFoundError
from daos.clients_dao_postgres import ClientDaoPostgres
import logging

app: Flask = Flask(__name__)
logging.basicConfig(filename="records.log", level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(message)s')

account_dao = AccountDaoPostgres()
account_service = AccountsServicesImpl(account_dao)
client_dao = ClientDaoPostgres()
client_service = ClientsServicesImpl(client_dao)


# CREATE
@app.route("/clients", methods=["POST"])
def post_client():
    body = request.json  # should I be passing in an id? Do I have to be passing in an id?
    client = Client(body["clientId"], body["bankMemberName"])
    client_service.post_client(client)
    return f"Created client {client.client_id}", 201


# READ
@app.route("/clients", methods=["GET"])
def get_all_client():
    client = client_service.get_all_client()
    json_client = [b.as_json_dict() for b in client]
    return jsonify(json_client), 200


@app.route("/clients/<client_id>", methods=["GET"])
def get_client(client_id: str):
    try:
        client = client_service.get_client(int(client_id))
        return jsonify(client.as_json_dict()), 200
    except ResourceNotFoundError as e:
        return str(e), 404


# UPDATE
@app.route("/clients/<client_id>", methods=["PUT"])
def put_client(client_id: str):
    body = request.json
    client = Client(body["clientId"], body["bankMemberName"])
    client.client_id = int(client_id)
    try:
        client_service.put_client(client)
        return "Update done", 200
    except ResourceNotFoundError as e:
        return str(e), 404


# DELETE
@app.route("/clients/<client_id>", methods=["DELETE"])
def delete_client(client_id: str):
    try:
        client_service.delete_client(int(client_id))
        return "Deleted Successfully", 205
    except ResourceNotFoundError as e:
        return str(e), 404


@app.route("/clients/<client_id>/accounts", methods=["POST"])
def post_account(client_id: str):
    body = request.json
    account = Account(body["accountId"], body["accountFunds"], body["accountType"], body["clientId"])
    account.client_id = int(client_id)
    output = account_service.post_account(account, int(client_id))
    if output is False:
        return f"No Client with ID {account.client_id} can not be found", 404
    else:
        return f"Created account {account.account_id}", 201


# READ
@app.route("/clients/<client_id>/accounts", methods=["GET"])
def get_all_account(client_id: str):
    less_than = request.args.get("amountLessThan")
    greater_than = request.args.get("amountGreaterThan")
    try:
        if less_than is not None and greater_than is not None:
            account = account_service.get_all_account_range(int(less_than), int(greater_than), int(client_id))
        else:
            account = account_service.get_all_account(int(client_id))
        json_account = [b.as_json_dict() for b in account]
        return jsonify(json_account), 200
    except ResourceNotFoundError as e:
        return str(e), 404


@app.route("/clients/<client_id>/accounts/<account_id>", methods=["GET"])
def get_account(client_id: str, account_id: str):
    try:
        account = account_service.get_account(int(account_id), int(client_id))
        return jsonify(account.as_json_dict()), 200
    except ResourceNotFoundError as e:
        return str(e), 404


# UPDATE

@app.route("/clients/<client_id>/accounts/<account_id>", methods=["PUT"])
def put_account(client_id: str, account_id: str):
    body = request.json
    account = Account(body["accountId"], body["accountFunds"], body["accountType"], body["clientId"])
    try:
        account_service.put_account(account, int(client_id), int(account_id))
        return "Update done", 200
    except ResourceNotFoundError as e:
        return str(e), 404
    except KeyError as e:
        return str(e), 404  # only error that is going off. Why?


# DELETE

@app.route("/clients/<client_id>/accounts/<account_id>", methods=["DELETE"])
def delete_account(client_id: str, account_id: str):
    try:
        account_service.delete_account(int(account_id), int(client_id))
        return "Deleted Successfully", 205
    except ResourceNotFoundError as e:
        return str(e), 404
    except KeyError as e:
        return str(e), 404  # only error that is going off. Why?


# PATCH
@app.route("/clients/<client_id>/accounts/<account_id>", methods=["PATCH"])
def withdraw_or_deposit_account(client_id: str, account_id: str):
    body = request.json
    for key in body:
        try:
            output = account_service.withdraw_or_deposit_account(int(account_id), key, body[key], int(client_id))
            return f"{key} Successful"
        except ResourceNotFoundError as e:
            return str(e), 404
        except KeyError as e:
            return str(e), 404
        except Exception as e:
            return str(e), 422


@app.route("/clients/<client_id>/accounts/<account_id_1>/transfer/<account_id_2>", methods=["PATCH"])
def transfer_account(client_id: str, account_id_1: str, account_id_2: str):
    body = request.json
    amount = body["amount"]
    try:
        output = account_service.transfer_account(int(account_id_1), int(account_id_2), int(amount), int(client_id))
        return f"Transfer of {amount} successful"
    except ResourceNotFoundError as e:
        return str(e), 404
    except KeyError as e:
        return str(e), 404
    except Exception as e:
        return str(e), 422


if __name__ == '__main__':
    app.run()
