# API Rate Limiter

## Summary
![overview](../img/api-rate-limiter-overview.png)

Once a new request arrives, the Web Server asks the Rate Limiter to decide if it will be served or throttled.

## Requirement

Functional requirements
 - Limit the number of requests an entity can send to an API within a time window.
- The APIs are accessible through a cluster, so the rate limit should be considered across different servers.
- The user should get an error message whenever the defined threshold is crossed within a single server or across a combination of servers.

Performance requirements
- The system should be highly available. The rate limiter should always work since it protects our service from external attacks.
- Our rate limiter should not introduce substantial latencies affecting the user experience.

## Throttling
- Throttling is the process of controlling the usage of the APIs by customers during a given period.
- Throttling can be defined at the application level and/or API level.
- When a throttle limit is crossed, the server returns HTTP status “429 - Too many requests".
- Types of throttling
  - Hard throttling: The number of API requests cannot exceed the throttle limit.
  - Soft throttling: we can set the API request limit to exceed a certain percentage.
  - Elastic / dynamic throttling: the number of requests can go beyond the threshold if the system has some resources available.

## Rate Limiting Algorithm

![window](../img/api-rate-limiter-window.svg)

- Fixed window: the time window is considered from the start of the time-unit to the end of the time-unit.
- Rolling window: the time window is considered from the fraction of the time at which each request is made plus the time window length.

## Fixed Window Solution
- Allow 3 requests per minute per user.
- Hashtable
  - Key: `userId`
  - Value: `count` and `startTime`
- Procedure for each request
  - For new user
    - Create a new entry
    - `count = 1`
    - `startTime = currentTime`
    - Allow the request.
  - For existing user
    - If `currentTime - startTime >= 1 min`, reset `count` and `startTime`.
    - Otherwise, reject the request if `count >= 3`, or allow the request if `count < 3` and increment `count`.
- Atomicity
  - In a distributed environment, the "read-and-then-write" behavior can create a race condition.
  - We can use lock, but it will slow concurrent requests from the same user, and introduce extra complexity.
- Memory usage
  - `userId`: 8B
  - `count`: 2B, count up to 65K
  - `startTime`: 4B; store only the minute and second part
  - lock: 4B number
  - hash overhead: 20 B
  - total: `(16B + 20B) * 1M users = 36 MB`
  - Can fit into one server, but should be distributed for performance reason
  - 3M QPS if the rate limit is 3 requests per user per second
- Implementation
  - Redis
  - Memcached

## Sliding Window Solution
- Hashtable
  - Key: `userId`
  - Value: sorted set of timestamps
- Procedure for each request
  - Remove all timestamps from the sorted set that are older than `currentTime - 1 min`
  - Reject the request if the total count is greater than throttling limit
  - Otherwise allow the request, and add the current time into the sorted set
- Memory usage
  - `userId`: 8B
  - each timestamp: 4B + 8B (prev pointer) + 8B (next pointer) = 20B
  - hash overhead: 20B
  - each user: `8B + 20B * 3 + 20B = 88B`
  - total: 88MB

## Sliding Window with Counters
- Keep track of request counts for each user using multiple fixed time windows.
- For example, for an hourly rate limit, we can keep a count for each minute and calculate the sum of all counters in the past hour.
- This will reduce memory footprint for large limites.
- For a rate limit of 500 requests per hour
  - Without counters: 8B user id + (4B timestamp + 20B sorted set overhead) * 500 timestamps + 20 hashtable overhead = 12KB
  - With counters: 8B user id + (4B timestamp + 2B count + 20B hash overhead) * 60 entries + 20B hashtable overhead = 1.6KB
  - 86% less memory

## Data Sharding
- Shard rate limiting data by `userId`.
- Use [consistent hashing](../basics/consistent-hashing.md).
- If different APIs have different limit, we can shard per user per API.

## Data Caching
- Application servers can quickly check if the cache has the desired record before hitting backend servers.
- Use [write-back cache](../basics/caching.md#cache-invalidation). The cache is persisted to persistence at fixed intervals.
- This is useful once the user has hit their max limit, and the rate limiter will only be reading data without any updates.

## Rate Limit by IP or by User
- By IP
  - Better than no rate limit at all.
  - When multiple users share a single public IP, one bad user can cause throttling to others.
  - There are a huge number of IPv6 addresses available from even one computer.
- By User
  - Performed after user authentication.
  - What about rate limit on the login API?
- Hybrid
  - Combine per-IP and per-user rate limiting.
  - Require more memory and storage.
