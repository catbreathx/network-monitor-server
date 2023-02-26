#!/bin/sh

psql postgresql://postgres:postgres@localhost:5432/postgres << EOF
  drop database if exists "network-monitor-e2e" (force);
  create database "network-monitor-e2e";
EOF
