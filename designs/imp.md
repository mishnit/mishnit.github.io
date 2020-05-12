1. Cache aside with LRU eviction policy - try to read form cache, if unavailable - read from DB and update cache 
2. SQL DB (frequent reads, i.e indexed columns, join required, read:write ratio being 10:1)- Write into active master and read from slave. Active Master will have async replication with Slave and passive master
3. NoSQL DB (frequent writes i.e, logs, clickstream data, write:read ratio being 10:1)- write & read from geo-specific shards
all shards (80-20 data replication)
