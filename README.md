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
