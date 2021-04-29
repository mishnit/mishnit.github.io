Functional Requirements: Post/tweet, Like, Share/retweet, Search, Follow, Timeline, Comment, trending
Non Functional Requirements: Low latency, High Availability
Scale: 150M DAU, 300M MAU, 1.5B Users, Read Heavy(100X of writes), 500M posts/day, 350K posts/min, 5K posts/sec on avg, 15k posts/sec at peak hours
User segmentation: Famous (most important), Live (important), active(less important), passive(inactive since last 3 days), inactive(soft delete)
Release cycles => Beta testing users, old users, new users 



Services=> User Service, Follow service, Post Service, Analytics Service


userdata flow from client -> LB1 -> Userservices-> userdata_cache (redis cluster)-> userdb (SQLdb cluster)
follow flow from client -> LB2 -> followservices -> followerdata_cache (redis cluster) -> follower/following db (graphdb/SQLdb geo shards) 
live user actions stream -> LB3 -> analyticsservices -> send event to message broker (Kafka) 
live user checker & notifier -> LB3 -> websocket connection <- notificationservices <- send notification based on events recieved onmessage broker (kafka) <- tweet proessor service <- cach
post tweet flow -> LB4 -> tweet injestion services (url shortener (KGS) + blob storage (s3) + metadata linking)-> tweetdb (cassandra) -> send event to message broker (kafka) -> tweet processor services (precompute timeline for active users) -> redis (active users timeline) 
timeline flow -> LB5 -> timeline service (fetch precomputed timeline from redis if available) -> else call user service + graph service (join data to compute timeline for user who just became active) -> redis-cache (active users timeline)gra


User Service
=============
Signup
Signin
getuserdetails
get analytics

Follow Service
===============
getfollowers
getfollowing
follow
unfollow


