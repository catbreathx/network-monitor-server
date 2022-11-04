#!/bin/sh

psql postgresql://postgres:postgres@localhost:5432/postgres << EOF
  drop database if exists "network-monitor";
  create database "network-monitor";
EOF

alembic upgrade head
