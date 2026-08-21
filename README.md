# 274B FinalProject
# Banking System

A python implementation of a banking system that supports account management, deposits, transfers, withdrawals, cashback payments, account merging, transaction history, and historical balance lookups.

The system tracks account balances and outgoing spending while also supporting scheduled transactions such as cashback refunds.

## Features

## Account Creation
Create a new bank account using a unique account identifier.

```python
create_account(timestamp, account_id)
```

Returns:
- True if the account was successfully created
- False if the account already exists

Each account tracks:
- Account ID
- Creation timestamp
- Current balance
- Total outgoing spending
- Account deletion/merge timestamp

---

## Deposits
Deposit money into existing account.

```python
deposit(timestamp, account_id, amount)
```

Returns the updated balance after the deposit

If the account does not exist, the method returns:

None

Deposits are also recorded in the account's transaction history.

---

## Transfers 

Transfer money between two accounts.

```python
transfer(
timestamp,
source_account_id,
target_account_id,
amount
)
```

A transfer succeeds only when:
- Both accounts exist
- The source and destination accounts are different
- The source account has sufficient funds

The transferred amount is deducted from the source amount and added to the destination account.

Outgoing transfers also contribute to the source account's total spending.

---

## Top Spenders

Retrieve the accounts with the highest total outgoing transactions.

```python
top_spenders(timestamp,n)
```

Resuts are returned in the following format:

```python
[
"account1(500)",
"account2(300)",
"account3(100)"
]
```

Accounts are ranked by:
1. Highest total amount spent
2. Alphabetical account ID when spending totals are tied

Outgoing spending includes transfers and withdrawals but does not include cashback refunds.

---

## Payments and Cashbaclk

Accounts can withdraw money using:

```python
pay(timestamp, account_id, amount)
```

A successful payment generates a unique payment ID:
```python
payment1
payment2
payment3
...
```

Payments deduct money from the account balance and contribute to the account's total outgoing spending.

### Cashback

Every successful withdrawal receives a 2% cashback reward.

The cashback amount. is calculated using:

```python
int(amount * 0.02)
```
Cashback is deposited back into the account exactly 24 hrs later.

The delay is represented as:

```python
86400000 milliseconds
```

Scheduled cashback transactions are stored in a priority queue using Pythons's heaps module so that the earliest scheduled transaction can be processed first.

---

## Payment Status

Payment status can be checked using:

```python
get_payment_status(timestamp, account_id, payment)
```

A payment can have one of two statuses:

IN_PROGRESS

or:

CASHBACK_RECEIVED

The payment begins as IN_PROGRESS and becomes CAHSBACK_RECEIVED once the scheduled cashback is processed.

---

## Scheduled Transaction Processing

Several banking methods use the updated_transactions decorator.

Before the requested banking operation executes, the decorator checks whether any scheduled cashback transactions are due.

If a cashback transaction has reached its scheduled timestamp, the system:

1. Retrieves the scheduled transaction
2. Adds the cashback amount to the appropriate account
3. Updates the payment status to CASHBACK_RECEIVED
4. Removes the transaction from the priority queue

This ensures that scheduled cashback is processed before other operations occurring at the same timestamp.

--- 

## Account Merging

Two accounts can be combined using:

```pyton
merge_accounts(
timestamp,
account_id_1,
account_id_2
)
```

account_id_2 is merged into account_id_1.

During a successful merge:
- The balance of account 2 is added to account 1
- The spending totals are combined
- Transaction histories are combined
- Pending cashback payments are redirected to account 1
- Account 2 is archived
- Account 2 is removed from the active account directory

The merge fails if:
- Both account IDs are identical
- Either account does not exist

Archived data is retained so that historical balance queries can still access information about merged accounts.

---

## Historical Balance Lookup

The system supports retrieving the balance of an account at an earlier timepoint.

```python
get_balance(timestamp, account_id, time_at)
```

The method reconstructs the account balance by examining transactions that occurred on or before time_at.

It also check whether:
- The account existed at the requested time
- The account had already been merged or deleted
- The requested timestamp occurred before the account was created

If the account did not exist at the requested time, the method returns:

None

---

## Data Structures

The implementation uses several Python data structures

### Dictionaries

self.accounts_dir
self.transactions
self.payments
self.archived_transactions
self.archived_accounts

Dictionaries provide fast lookup of accounts, transactions, and payments using identifiers.

### Lists
self.sorted_spenders
self.completed_transactions

Lists are used to maintain account rankings and transaction collections

### Priority Queue
self.scheduled_transactions

Scheduled cashback transactions are maintained using Python's heapq.

Because transactions implement:

```python
def__lt__(self, other):
return self.timestamp < other.timestamp
```

the heap automatically prioritizes the transaction with the earliest timestamp.

---

## Classes

### BankingSystemImpl

The primary banking system class

It manages:
- Accounts
- Transactions
- Deposits
- Transfers
- Payments
- Cashback
- Spending rankings
- Account merging
- Historical balances

---

### Account

Represents an individual banking acocunt

Each account stores:

```python
timestamp
balance
account_id
spent
deltime
```

Example:
```python
account = Account(
account_id = "Alice",
timestamp = 1
)
```

---
### Transaction

Represents a banking transaction.

Each transaction stores:

```python
source_id
timestamp
amount
status
payment_id
```

Transactions are comparable by timestamp, which allows them to be stored in a priority queue.

---

## Example Usage

```python
bank = BankingSystemImpl()

bank.create_account(1,"Alice")
bank.create_account(2,"Bob")

bank.deposit(3,"Alice",1000)

bank.transfer(
4,
"Alice",
"Bob",
200
)

payment_id = bank.pay(
5,
"Alice",
100
)

print(payment_id)
```

Example output

```python
payment1
```

Check the payment:

```python
status = bank.get_payment_status(
6,
"Alice",
payment_id
)

print(status)
```

Output:

IN_PROGRESS

After the cashback timestamp is reached, the status becomes:

CASHBACK_RECEIVED

---

## Project Structure

A typical project layout looks like:
│
├── banking_system.py
├── banking_system_impl.py
├── tests/
│   └── test_banking_system.py
└── README.md

The implementation currently defines the Account and Transaction classes alongside banking_system_impl

---

## Requirements

- python 3.10+
- Standard Python library

The implementation uses:

```python
import heapq
```

--- 

## Key Concepts Demonstracted

This project demonstrates several important programming and data-structure concepts
- Object-oriented programming
- Dictionaries and hash-based lookup
- Priority queues/ heaps
- Transaction history
- Scheduled event processing
- Decorators
- Custom object comparison
- Sorting with custom keys
- State management
- Historical data reconstruction

---

## Notes
Scheduled cashback processing is integrated into banking operations using a decorator. This allows pending transactions to be processed automatically before operations such as deposits, transfers, payments, and account queries.
The system also maintains archived account and transaction information so historical queries can continue to work after accounts have been merged.




