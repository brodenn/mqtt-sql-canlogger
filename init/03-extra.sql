-- 📈 Max & min per topic senaste 10 minuterna
CREATE OR REPLACE VIEW extremes_recent AS
SELECT
  topics.name AS topic,
  MAX(CASE WHEN topics.name = 'canbus/speed' THEN payload::numeric END) AS max_speed,
  MIN(CASE WHEN topics.name = 'canbus/temp' THEN payload::numeric END) AS min_temp
FROM messages
JOIN topics ON messages.topic_id = topics.id
WHERE timestamp > now() - interval '10 minutes';
