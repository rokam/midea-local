#!/usr/bin/env bash
# Setups the repository.

# Stop on errors
set -e

pre-commit install
pre-commit install --hook-type commit-msg
cd
npm install @commitlint/config-conventional
