#!/usr/bin/env bash
cd "$(dirname "$0")/../backend"
uvicorn cofreseguro.main:app --reload --port 8080
