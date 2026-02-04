# SurrealDB Setup Guide

This guide explains how to set up the SurrealDB namespace, database, and user for the **Sage** service.

In SurrealDB, the hierarchy is Namespace -> Database.

Here is the equivalent mapping:

CREATE DATABASE -> DEFINE NAMESPACE + DEFINE DATABASE
CREATE USER -> DEFINE USER ... ON DATABASE

## 1. Quick Setup Script
We have provided a script at `sage/setup.surql`.

```sql
-- 1. Create a logical group (Namespace)
DEFINE NAMESPACE sage_ns;
USE NAMESPACE sage_ns;

-- 2. Create the database inside it
DEFINE DATABASE sage_db;
USE DATABASE sage_db;

-- 3. Create the user "sage" with full access (OWNER) *only* to this DB
DEFINE USER sage ON DATABASE PASSWORD 'pass' ROLES OWNER;
```

## 2. Running the Script

You can run this against your local SurrealDB instance using the CLI:

```bash
# Assuming SurrealDB is running on port 8000
# Authentication: root/root (default)
surreal sql --endpoint http://localhost:8000 --user root --pass root --ns test --db test < sage/setup.surql
```

## 3. Configuration Update

After running the script, update your `.env` file in `sage/` to match the new credentials:

```ini
# sage/.env

SURREAL_URL=ws://localhost:8000/rpc
SURREAL_USER=sage
SURREAL_PASS=pass
SURREAL_NS=sage_ns
SURREAL_DB=sage_db
```

## 4. Verification

You can verify the connection by running:
```bash
npm run dev:sage
```
Check the logs for successful connection messages.
