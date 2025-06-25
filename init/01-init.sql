-- 🔧 Tabell: Topics
CREATE TABLE IF NOT EXISTS topics (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

-- 📨 Tabell: Messages
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    topic_id INTEGER REFERENCES topics(id),
    timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    payload TEXT NOT NULL
);