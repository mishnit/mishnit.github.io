1. Cache aside with LRU eviction policy - try to read form cache, if unavailable - read from DB and update cache 
2. SQL DB (frequent reads, i.e indexed columns, join required, read:write ratio being 10:1)- Write into active master and read from slave. Active Master will have async replication with Slave and passive master
3. NoSQL DB (frequent writes i.e, logs, clickstream data, write:read ratio being 10:1)- write & read from geo-specific shards
all shards (80-20 data replication)



* DB architecture 1: (master slave replication is lazy but eventual consistent)

passive_master_global--------l-----------------active_master_global-------------------slave1_global---------slave2_global
(stand_by 1-1000)                                 (write 1-1000)                      (read 1-1000)       (read 1-1000)
                                               /         |        \
                                         /               |              \
                                    /                    |                    \
                    shard_master_india            shard_master_SEA              shard_master_LatAm
                    (lazy write 1-333)           (lazy write 334-667)             (lazy write 667-1000)
                           /    \                        /    \                           /    \
                          /      \                      /      \                         /      \
            shard_slave_delhi   shard_slave_mumbai     ..........           shard_slave_peru    shard_slave_columbia
              (read 1-333)        (read 1-333)                               (read 667-1000)      (read 667-1000)



* At scale: (Read requests gets load balanced across all shard-slaves for the geo from where request is being made) 

passive_master_india--------l-----------------active_master_india-------------------slave1_india---------slave2_india
(stand_by 1-333)                                 (write 1-333)                     (read 1-333)          (read 1-333)
                                               /         |        \
                                         /               |              \
                                    /                    |                    \
                    shard_master_india           shard_master_india             shard_master_india
                     (lazy write 1-111)          (lazy write 112-222)            (lazy write 223-333)
                           /    \                        /    \                           /    \
                          /      \                      /      \                         /      \
          shard_slave_delhi   shard_slave_mumbai       ..........          shard_slave_delhi    shard_slave_mumbai
            (read 1-111)        (read 1-111)                                 (read 223-333)      (read 223-333)
         
         
 
 
 
 
 
 
 
 
 
 
 
 
