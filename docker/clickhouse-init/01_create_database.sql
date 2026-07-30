-- Create the raglens database on ClickHouse first boot.
-- Table DDL lives in backend/migrations/clickhouse/ and is applied at backend startup.
CREATE DATABASE IF NOT EXISTS raglens;
