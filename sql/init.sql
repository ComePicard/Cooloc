CREATE TABLE IF NOT EXISTS users (
    id ULID PRIMARY KEY DEFAULT gen_ulid(),
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    age INT CHECK (age >= 0),
    adress VARCHAR(255),
    phone_number VARCHAR(15) UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS groups (
    id ULID PRIMARY KEY DEFAULT gen_ulid(),
    name VARCHAR(50) NOT NULL,
    description TEXT,
    city VARCHAR(50),
    postal_code VARCHAR(10),
    country VARCHAR(50),
    contact_email VARCHAR(100) NOT NULL,
    contact_phone VARCHAR(15),
    agency_email VARCHAR(100),
    agency_phone VARCHAR(15),
    starting_at TIMESTAMP,
    ending_at TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS documents (
    id ULID PRIMARY KEY DEFAULT gen_ulid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    file_path VARCHAR(255) NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    owner_id ULID REFERENCES users(id) ON DELETE CASCADE,
    group_id ULID REFERENCES groups(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS spendings (
    id ULID PRIMARY KEY DEFAULT gen_ulid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    owner_id ULID REFERENCES users(id) ON DELETE CASCADE,
    group_id ULID REFERENCES groups(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS users_groups (
    user_id ULID REFERENCES users(id) ON DELETE CASCADE,
    group_id ULID REFERENCES groups(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, group_id)
);

CREATE TABLE IF NOT EXISTS users_documents (
    user_id ULID REFERENCES users(id) ON DELETE CASCADE,
    document_id ULID REFERENCES documents(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, document_id)
);

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER users_set_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER groups_set_updated_at
BEFORE UPDATE ON groups
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER documents_set_updated_at
BEFORE UPDATE ON documents
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER spendings_set_updated_at
BEFORE UPDATE ON spendings
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

