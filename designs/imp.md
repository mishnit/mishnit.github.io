ssssh its secret.... just go to edit mode and everything would be visible



* Sharded Master-Slave architecture: 

1. Write happens in master and read happens from slave replicas.
2. master-slave replication is lazy but eventual consistent.
2. shard-slave replication for same geo is lazy and will always have 80/20 data ratio.
3. Also, If the master shard fails, an automatic failover happens and the slave shard is promoted to be the new master shard.
4. Read requests gets load balanced across all shard-slaves for the geo from where request is being made.
5. All shard slave for same geo will be accesible using load balancer with consistent hashing algo.
6. First read from geo cache (cache_ind), if not available read from geo shard-slave (shard_slave_india) using consistent hashing at load balancer, then update geo_cache (cache_ind). 
 
 
 
 

passive_master_global-------------------------active_master_global
(stand_by 1-1000)                                 (write 1-1000)
                                               /         |        \
                                         /               |              \
                                    /                    |                    \
                    shard_master_global           shard_master_global             shard_master_global
                     (lazy write 1-333)          (lazy write 334-666)            (lazy write 667-1000)
                           /    \                        /    \                           /    \
                          /      \                                                       /      \
          shard_slave_india.......\.........<consistent_hashing>..........shard_slave_india      \
            (read 1-333)           \                                      (read 667-1000)        \
                                    \                                                             \
                                   shard_slave_usa..........<consistent_hashing>.... .............shard_slave_usa 
                                   (read 1-333)                                                   (read 667-1000)
         
        
 
 
 
 
 
 
 
 
 
 
 
 