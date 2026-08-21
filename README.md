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
