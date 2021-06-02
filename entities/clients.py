# Clients of First Totally Real Bank of Town

class Client:

    # Visualise how many accounts by SQL returning how many accounts mach with client's ID
    def __init__(self, client_id: int, bank_member_name: str):
        self.client_id = client_id
        self.bank_member_name = bank_member_name

    def as_json_dict(self):
        return {"clientId": self.client_id,
                "bankMemberName": self.bank_member_name
                }
