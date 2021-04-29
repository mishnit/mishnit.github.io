Functional Requirements: Post/tweet, Like, Share/retweet, Search, Follow, Timeline, Comment, trending

Non Functional Requirements: Low latency, High Availability

Scale: 150M DAU, 300M MAU, 1.5B Users, Read Heavy(100X of writes), 500M posts/day, 350K posts/min, 5K posts/sec on avg, 15k posts/sec at peak hours

User segmentation: Famous (most important), Live (important), active(less important), passive(inactive since last 3 days), inactive(soft delete) 



Services=> User Service, Follow service, Tweet Service, Timeline service, Notification service, Search service, Analytics Service, trend service


HLD
----

userdata flow from client -> LB1 -> Userservice (read from cache first, write int db first) -> userdata_cache (redis cluster) -> userdb (write master- read slaves cluster)

follow flow from client -> LB2 -> followservice (read from cache first, write int db first -> followerdata_cache (redis cluster) -> follower/following db (graphdb/SQLdb write master- read slaves cluster) 

live user actions stream -> LB3 -> analyticsservice -> send event to message broker (Kafka topic: action) -> stream proceesing service(spark cluster) -> analytics db (hadoop) -> weekly cron service -> weekly/monthly reports

live user notifier -> LB3 -> websocket connection <- notificationservice <- message broker (kafka topic: tweet) <- tweet processor service <- activeuserstimeline_cache (redis cluster)

post tweet flow -> LB4 -> tweet injestion service (url shortener (KGS) + blob storage (S3) + metadata linking)-> tweetdb (cassandra cluster) -> tweet service -> message broker (kafka topic: tweet) -> timeline services (save precomputed timeline for active and famous users) -> activeuserstimeline_cache (redis cluster) 

get timeline flow -> LB5 -> timeline service (fetch precomputed timeline from activeuserstimeline_cache if available) -> else call user service + graph service (join data to compute timeline for user who just became active) -> activeuserstimeline_cache (redis cluster)

search flow -> LB6 -> search service -> searchdata_cache (redis cluster) -> searchdb (elastic search cluster) -> search consumer ->  message broker (kafka topic: tweet)

trending -> LB7 -> trend service -> trendingdata_cache (redis cluster) -> stream proceesing service(spark cluster) -> trends db (mongodb)



