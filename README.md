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

