# Runbook step 135

## Goal
Operational check #135 for CofreSeguro demo/production readiness.

## Steps
1. Confirm API `/health` returns healthy.
2. Confirm `/ready` can reach the database.
3. Login as demo user and analyze sample message #135.
4. Verify history entry and behavioural counters update.
5. Capture screenshot for presenter notes (Android or Web).

## Rollback
Restart API container; clear local SQLite only in demo environments.
