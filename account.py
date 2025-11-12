import datetime

class Account:
    '''
    Implementation of the Account class. After the BankingSystem class creates an account, an
    instance of the Account class is created.
    '''
    def __init__(self, account_id: str, timestamp: int, balance = 0.0):
        self.timestamp = timestamp  #2025-11-11 18:27:09.095745
        self.balance = balance
        self.account_id = account_id
        self.spent

        