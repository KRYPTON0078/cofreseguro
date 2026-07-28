# API reference

## Auth
- `POST /v1/auth/register`
- `POST /v1/auth/login` (returns access + refresh)
- `POST /v1/auth/refresh`
- `POST /v1/auth/logout`
- `POST /v1/auth/change-password`
- `GET /v1/auth/me`

## Analyze
- `POST /v1/analyze`
- `POST /v1/analyze/image`
- `GET /v1/history`
- `GET /v1/history/{id}`
- `DELETE /v1/history/{id}`

## Tips / Behaviour / Feedback / Admin
- `GET /v1/tips`
- `GET /v1/tips/by-label/{label}`
- `GET /v1/behaviour/me`
- `POST /v1/feedback`
- `GET /v1/admin/users`
- `GET /v1/admin/analyses/recent`
- `POST /v1/admin/policies/reload`
- `GET /v1/admin/metrics/summary`

## Ops
- `GET /health`
- `GET /ready`
- `GET /metrics`
