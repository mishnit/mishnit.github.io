Functional Requirements: Book Cab, ETA, Cab tracking

Non Functional Requirements: Low latency, High Availability, Dispatch optimisation

Scale: 50M DAU, 100M MAU, 15M rides/day

User segmentation: Driver, User

Services=> User Service, Driver service, Cab Request service, Cab Finder service, Location service


HLD
----

userdata flow from user -> LB1 -> Userservice (read from cache first, write int db first) -> userdata_cache (redis cluster) -> userdb (write master- read slaves cluster)

cab request matching flow from user -> LB2 -> cabrequestservice (computes avg price based on volume of driver availabilty, distance, surge etc ) -> cabfinderservice (pull location of nearby available drivers and assign priority) -> message broker (kafka topic: drivers_available) 

trip tracking + ETA flow from user -> LB3 -> 

driverdata flow from driver -> LB4 -> Driverservice (read from cache first, write int db first) -> driverdata_cache (redis cluster) -> driverdb (write master- read slaves cluster)

location ping (every 3sec) from on-trip driver -> LB5 -> Websocket handlers along with websocket manager -> LB3 -> location service (uses quadtree for spatial indexing) -> locationdata_cache (redis cluster) 
