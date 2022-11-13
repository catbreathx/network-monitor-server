#!/bin/sh

psql postgresql://postgres:postgres@localhost:5432/postgres << EOF
  drop database if exists "network-monitor";
  create database "network-monitor";
EOF

alembic upgrade head

python -m scripts.admin --email admin@user.com --first-name=admin --config-file dev.env  --password 1.Password01.

psql postgresql://postgres:postgres@localhost:5432/network-monitor << EOF
  update public.user set account_confirmed=true, enabled=true
EOF
