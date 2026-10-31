-- Extra database for Konga UI metadata (Kong itself uses POSTGRES_DB=kong).
CREATE DATABASE konga;
GRANT ALL PRIVILEGES ON DATABASE konga TO kong;
