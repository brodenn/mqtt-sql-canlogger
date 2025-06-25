-- 👁️ View 1: Senaste meddelandet per topic
CREATE OR REPLACE VIEW latest_per_topic AS
SELECT DISTINCT ON (topics.name)
  topics.name AS topic,
  messages.payload,
  messages.timestamp
FROM messages
JOIN topics ON messages.topic_id = topics.id
ORDER BY topics.name, messages.timestamp DESC;

-- 📊 View 2: Antal meddelanden per minut (senaste 10 minuterna)
CREATE OR REPLACE VIEW messages_per_minute AS
SELECT
  date_trunc('minute', timestamp) AS minute,
  topics.name AS topic,
  COUNT(*) AS message_count
FROM messages
JOIN topics ON messages.topic_id = topics.id
WHERE timestamp > now() - interval '10 minutes'
GROUP BY minute, topics.name
ORDER BY minute DESC, topic;

-- 📉 View 3: Genomsnittlig hastighet och temperatur senaste 5 minuterna
CREATE OR REPLACE VIEW avg_recent_values AS
SELECT
  ROUND(AVG(CASE WHEN topics.name = 'canbus/speed' THEN payload::numeric END), 1) AS avg_speed,
  ROUND(AVG(CASE WHEN topics.name = 'canbus/temp' THEN payload::numeric END), 1) AS avg_temp
FROM messages
JOIN topics ON messages.topic_id = topics.id
WHERE timestamp > now() - interval '5 minutes';
