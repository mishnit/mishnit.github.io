Functional requirements: Hotel/Restro onboarding, hotel/restro manager can see bookings, User can search & filter hotel/restro for given criteria, user can book/cancel/update room/table for specific capacity for specific time period on a date, charge users for booking to reduce no-shows and refund same post billing

Non functional requirements: Low latency, High availability

Scale: 500k hotels/restro, 10M rooms/tables, 

Services: User service, Hotel/restro service, Booking service, search service, payment service, notification service, Booking Management Service

HLD
----

(a) User onboarding and profile data flow from user app -> LB1 -> Userservice (read from cache first, write int db first) -> userdata_cache (redis cluster) -> userdb (write master- read slaves cluster)

(b) hotel/restro onboarding and profile data flow from hotel/restro app -> LB2 -> H/R_service (read from cache first, write int db first, once written push the data to message broker as producer) -> H/R_data_cache (redis cluster) -> H/R_db (write master- read slaves cluster) -> message broker (Kafka topic: new_hotel) 

(c) hotel search flow from user app -> LB3 -> Search Service -> searchdata_cache (redis cluster) -> searchdb (elastic search cluster) -> search consumer pulls new hotels and aggragate to make them searchable on date, loc, name, category, cuisine, etc -> message broker (kafka topic: new_hotel)

(d) booking flow from user app -> LB4 -> Booking Service (saves booking data in DB and send sync requests waiting for payment to finish)-> Payment Service (comfirms payment success/failure to booking service)->  
