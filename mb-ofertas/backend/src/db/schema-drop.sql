-- MB-OFERTAS - Apagar tudo e recomeçar do zero
-- Execução: npm run db:drop (ou node --loader ts-node/esm src/db/drop.ts)
-- Depois rode: npm run db:migrate para recriar com schema.sql

-- Ordem: tabelas com FK primeiro (filhas), depois pais
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS send_counters;
DROP TABLE IF EXISTS campaigns;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS categories;
