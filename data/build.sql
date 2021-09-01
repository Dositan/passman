CREATE TABLE IF NOT EXISTS passwords (
    id SERIAL PRIMARY KEY,
    network VARCHAR(20) PRIMARY KEY,
    email VARCHAR(100),
    content VARCHAR(50),
    saved_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC')
);

$$LANGUAGE plpgsql;