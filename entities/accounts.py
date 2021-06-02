# Accounts of First Totally Real Bank of Town

class Account:

    def __init__(self, account_id: int, account_funds: float, account_type: str, client_id: int):
        self.account_id = account_id
        self.client_id = client_id
        self.account_funds = account_funds
        self.account_type = account_type

    def as_json_dict(self):
        return {"accountId": self.account_id,
                "clientID": self.client_id,
                "accountType": self.account_type,
                "accountFunds": self.account_funds
                }
