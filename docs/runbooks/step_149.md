# Runbook step 149

## Goal
Operational check #149 for CofreSeguro demo/production readiness.

## Steps
1. Confirm API `/health` returns healthy.
2. Confirm `/ready` can reach the database.
3. Login as demo user and analyze sample message #149.
4. Verify history entry and behavioural counters update.
5. Capture screenshot for presenter notes (Android or Web).

## Rollback
Restart API container; clear local SQLite only in demo environments.
