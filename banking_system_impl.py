from banking_system import BankingSystem
from account import Account
from transaction import Transaction
import heapq 
import pdb
class BankingSystemImpl():

    def __init__(self):
        # TODO: implement
        self.accounts_dir = dict() # account directory
        self.transactions = dict() # transaction directory
        self.payments = dict() # payment directory
        self.clock = 0
        self.scheduled_transactions = [] #(Transaction(account_id...))
        self.completed_transactions = []
        self.num_payments = 0
        self.sorted_spenders = []

    def create_account(self, timestamp: int, account_id: str) -> bool:
        """
        Should create a new account with the given identifier if it
        doesn't already exist.
        Returns `True` if the account was successfully created or
        `False` if an account with `account_id` already exists.
        """
        self.clock = timestamp
        # implementation
        if account_id in self.accounts_dir:
            return False
        else:
            self.accounts_dir[account_id] = Account(account_id, timestamp) 
            self.transactions[account_id] = []
            self.sorted_spenders.append(self.accounts_dir[account_id])          
            return True
    
    def update_transactions(func):
        """class method that updates the banking system's scheduled payments"""
        def decorator_update_transactions(self, *args, **kwargs):
            if self.scheduled_transactions:
                timestamp = args[0] #current timestamp
                while self.scheduled_transactions and self.scheduled_transactions[0].timestamp <= timestamp:
                    #print(args[0])
                    transaction = self.scheduled_transactions[0]
                    #removed
                    #since the cash back is already part of the account transactions;
                    #avoid creating a duplicate deposit by manually updating balance
                    #this is important for the later get_balance implementation
                    #self.deposit(transaction.timestamp, transaction.source_id, transaction.amount)
                    curr_account = self.accounts_dir[transaction.source_id]
                    curr_account.balance += transaction.amount
                    og_transaction = self.payments[transaction.payment_id]
                    og_transaction.status = "CASHBACK_RECEIVED"
                    heapq.heappop(self.scheduled_transactions)
                    #removed if statement; rolled into while loop with <=

            self.sorted_spenders = sorted(self.sorted_spenders, key = lambda s: (-s.spent, s.account_id))
            result = func(self,*args, **kwargs)
            return result
        return decorator_update_transactions
   
    @update_transactions
    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        """
        Should deposit the given `amount` of money to the specified
        account `account_id`.
        Returns the balance of the account after the operation has
        been processed.
        If the specified account doesn't exist, should return
        `None`.
        """
        #  implementation
        self.clock = timestamp
        acct = self.accounts_dir.get(account_id)
        if acct is None:
            return None
        acct.balance += amount
        #heapq.heappush_max(self.completed_transactions, Transaction(account_id, amount, timestamp))
        #heapq.heapify_max(self.completed_transactions)

        return acct.balance

    @update_transactions
    def transfer(self, timestamp: int, source_account_id: str, target_account_id: str, amount: int) -> int | None:
        """
        Should transfer the given amount of money from account
        `source_account_id` to account `target_account_id`.
        Returns the balance of `source_account_id` if the transfer
        was successful or `None` otherwise.
          * Returns `None` if `source_account_id` or
          `target_account_id` doesn't exist.
          * Returns `None` if `source_account_id` and
          `target_account_id` are the same.
          * Returns `None` if account `source_account_id` has
          insufficient funds to perform the transfer.
        """
        #  implementation
        src = self.accounts_dir.get(source_account_id)
        heapq.heappush(self.completed_transactions, Transaction(source_account_id, amount, timestamp))
        heapq.heapify(self.completed_transactions)
        dst = self.accounts_dir.get(target_account_id)
        if src is None or dst is None or source_account_id == target_account_id:
            return None
        if src.balance < amount:
            return None
        src.balance -= amount
        src.spent += amount
        self.deposit(timestamp, target_account_id, amount)
        return src.balance

    @update_transactions
    def top_spenders(self, timestamp: int, n: int) -> list[str]:
        """
        Should return the identifiers of the top `n` accounts with
        the highest outgoing transactions - the total amount of
        money either transferred out of or paid/withdrawn (the
        **pay** operation will be introduced in level 3) - sorted in
        descending order, or in case of a tie, sorted alphabetically
        by `account_id` in ascending order.
        The result should be a list of strings in the following
        format: `["<account_id_1>(<total_outgoing_1>)", "<account_id
        _2>(<total_outgoing_2>)", ..., "<account_id_n>(<total_outgoi
        ng_n>)"]`.
          * If less than `n` accounts exist in the system, then return
          all their identifiers (in the described format).
          * Cashback (an operation that will be introduced in level 3)
          should not be reflected in the calculations for total
          outgoing transactions.
        """
        #implementation
        #return []
        
        return [f"{s.account_id}({s.spent})" for s in self.sorted_spenders[:n]]

        '''
        pairs = []
        for acc_id, act in self.accounts_dir.items():
            pairs.append ((acc_id,acc.outgoing))
        pairs.sort(key=lambda x: (-x[1],x[0]))
        result =[]
        for acc_id, total in pairs[:max(0, n)]:
            result.append(f"{acct_id({total})}")
        
        return result
        
        #pseduocode bd test wrapper
       """ 
       class Spender:
            def_init__(self, account_id:str, out)
            self.account_id = account_id
            self.outgoing = outgoing
            
       def top_spenders(self, timestamp: int, n: int) -> list[str]:
           spender = []
           for account_id, acc in self.accounts_dir.items():
               spenders.append(Spender(acc_id, acc.outgoing))
               
            spenders.sort(key=lamba s: (-s.outgoing, s.account_id))
           return [f"{s.account_id}({s.outgoing})" for s in spenders[:n]]"""
        '''
    @update_transactions
    def pay(self, timestamp: int, account_id: str, amount: int) -> str | None:
        """
        Should withdraw the given amount of money from the specified
        account.
        All withdraw transactions provide a 2% cashback - 2% of the
        withdrawn amount (rounded down to the nearest integer) will
        be refunded to the account 24 hours after the withdrawal.
        If the withdrawal is successful (i.e., the account holds
        sufficient funds to withdraw the given amount), returns a
        string with a unique identifier for the payment transaction
        in this format:
        `"payment[ordinal number of withdraws from all accounts]"` -
        e.g., `"payment1"`, `"payment2"`, etc.
        Additional conditions:
          * Returns `None` if `account_id` doesn't exist.
          * Returns `None` if `account_id` has insufficient funds to
          perform the payment.
          * **top_spenders** should now also account for the total
          amount of money withdrawn from accounts.
          * The waiting period for cashback is 24 hours, equal to
          `24 * 60 * 60 * 1000 = 86400000` milliseconds (the unit for
          timestamps).
          So, cashback will be processed at timestamp
          `timestamp + 86400000`.
          * When it's time to process cashback for a withdrawal, the
          amount must be refunded to the account before any other
          transactions are performed at the relevant timestamp.
        """
        # for our implementation, withdrawal + scheduled payment part
        #  implementation
        # check for account
        if self.accounts_dir.get(account_id, Account(-1, -1, 0) ).balance >= amount:
                # make transaction
            transaction = Transaction(account_id, -amount, timestamp)
            self.transactions.get(account_id).append(transaction)
            self.num_payments +=1
            acct = self.accounts_dir.get(account_id)
            acct.spent += amount
            acct.balance -= amount
            #transaction.status = "IN_PROGRESS"
            #transaction.cashback_timestamp = timestamp + 86400000
            #no need for a cashback timestamp; treat the cashback as its on transaction with the cashback time as timestamp
            payment_id = f"payment{self.num_payments}"
            future_deposit = Transaction(account_id, int(amount * .02), 
                                         timestamp + 86400000, payment_id=payment_id, processed="IN_PROGRESS")
            self.transactions.get(account_id).append(future_deposit)
            #print(f"{transaction.cashback_timestamp}: {account_id}, balance: {acct.balance}, cashback: {int(amount * 0.02)}")
            #self.transactions.get(account_id, future_deposit)
            #push onto heap
            heapq.heappush(self.scheduled_transactions, future_deposit)
            #heapq.heapify(self.scheduled_transactions)
            #payment_id = f"payment{self.num_payments}"
            self.payments[payment_id] = future_deposit
            return payment_id
        else:
            return None

    @update_transactions
    def get_payment_status(self, timestamp: int, account_id: str, payment: str) -> str | None:
        """
        Should return the status of the payment transaction for the
        given `payment`.
        Specifically:
          * Returns `None` if `account_id` doesn't exist.
          * Returns `None` if the given `payment` doesn't exist for
          the specified account.
          * Returns `None` if the payment transaction was for an
          account with a different identifier from `account_id`.
          * Returns a string representing the payment status:
          `"IN_PROGRESS"` or `"CASHBACK_RECEIVED"`.
        """
        #  implementation
        """if self.accounts_dir.get(account_id) is None:
            return None
        elif self.payments.get(payment) is None:
            return None
        elif self.payments.get(payment).source_id != account_id:
            return None
        else:
            if timestamp < self.completed_transactions[-1]:
                pass # check the most recently added value to the heapq
            else:
                transaction = self.payments.get(payment)
                return transaction.status"""
        
        transaction = self.payments.get(payment)
        acc = self.accounts_dir.get(account_id)
        if transaction is None or acc is None or transaction.source_id != account_id:
            return None
        
        return transaction.status

        
    def merge_accounts(self, timestamp: int, account_id_1: str, account_id_2: str) -> bool:
        """
        Should merge `account_id_2` into the `account_id_1`.
        Returns `True` if accounts were successfully merged, or
        `False` otherwise.
        Specifically:
          * Returns `False` if `account_id_1` is equal to
          `account_id_2`.
          * Returns `False` if `account_id_1` or `account_id_2`
          doesn't exist.
          
          * All pending cashback refunds for `account_id_2` should
          still be processed, but refunded to `account_id_1` instead.
          
          * After the merge, it must be possible to check the status
          of payment transactions for `account_id_2` with payment
          identifiers by replacing `account_id_2` with `account_id_1`.

          * The balance of `account_id_2` should be added to the
          balance for `account_id_1`.

          * `top_spenders` operations should recognize merged accounts
          - the total outgoing transactions for merged accounts should
          be the sum of all money transferred and/or withdrawn in both
          accounts.
          * `account_id_2` should be removed from the system after the
          merge.
        """
        #  implementation
        if account_id_1 == account_id_2:
            return False
        if account_id_1 is None or account_id_2 is None:
            return False
        if not account_id_1 or not account_id_2:
            return False


        for i in self.scheduled_transactions:
            print(i)
            if i.source_id == account_id_2:
                i.source_id = account_id_1

        acct1 = self.accounts_dir.get(account_id_1)
        acct2 = self.accounts_dir.get(account_id_2)
        if acct1 is None or acct2 is None:
            return False

        acct1.balance += acct2.balance
        acct1.spent += acct2.spent
        print(f"Account id changed, merged {account_id_2} into {account_id_1}")

        self.accounts_dir.pop(account_id_2,None)

        self.sorted_spenders = [ acc for acc in self.sorted_spenders if acc.account_id != account_id_2]

        return True

    @update_transactions
    def get_balance(self, timestamp: int, account_id: str, time_at: int) -> int | None:
        """
        Should return the total amount of money in the account
        `account_id` at the given timestamp `time_at`.
        If the specified account did not exist at a given time
        `time_at`, returns `None`.
          * If queries have been processed at timestamp `time_at`,
          `get_balance` must reflect the account balance **after** the
          query has been processed.
          * If the account was merged into another account, the merged
          account should inherit its balance history.
        """
        #  implementation
        account_transactions = self.transactions.get(account_id)
        if account_transactions is None:
            return None
        if self.accounts_dir.get(account_id).timestamp > time_at: # creation of account is after time_at
            return None
        pass
    
    
            # deposit()
            # timestamp: int, account_id: str, amount: int
    

    # TODO: implement interface methods here
# bofa = BankingSystemImpl()
# bofa.create_account(1,"account1")