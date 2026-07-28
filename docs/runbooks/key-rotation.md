# Runbook: key-rotation

Set new JWT_SECRET, restart pods, revoke refresh tokens, notify clients to re-login.

## Checks

1. /health
2. /ready
3. Demo login
