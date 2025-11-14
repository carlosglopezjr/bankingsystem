from account import Account

class Transaction:
    '''
    Abstract class for account transactions
    '''
    def __init__(self, account_id: str, amount: int, timestamp: int, payment_id = "N/A"):
        self.source_id = account_id # source account id
        self.timestamp = timestamp
        self.amount = amount
        self.status = "Processed" # changed for 
        self.cashback_timestamp = 0 # default for all non-scheduled payment transactions
        self.payment_id = payment_id

    #def __eq__(self, other):

    def __lt__(self, other):
        return self.timestamp < other.timestamp

    def __str__(self):
        return f"transaction timestamp: {self.timestamp}, amount: {self.amount}, accountid: {self.source_id}"
    
'''
class Deposit (Transaction):
    def __init__(self,account_id,amount):
        super().__init__(self,account_id,amount,timestamp)

class Withdrawal (Transaction):
    def __init__(self, account_id: str, amount: int, timestamp: int):
        super().__init__(self, account_id, amount, timestamp)

class ScheduledPayment (Transaction):
    def __init__(self, account_id: str, amount: int, timestamp: int, status):
        self.account_id = account_id
'''