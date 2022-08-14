Functional requirements:
vendor (hotel/restro) onboarding
vendor info can be updated in system 
vendor (hotel/restro) manager can view bookings
User Onboarding
Users can search & filter vendors (hotel/restro) for given criteria (roomtype/cuisine) along with location and datetime
users can book/view/cancel/update their bookings (room/table) for specific capacity for specific datetime slot
vendor can charge users for booking to reduce no-shows and refund same post billing

Non functional requirements: 
Low latency
High availability
Row level locks to avoid race condition while blocking the slot

Scale:
500k vendors(hotels/restros)
10M iteneries(rooms/tables) 

Out of scope: Analytics 

Services: User service, Vendor(hotel/restro) service, Booking service, search service, payment service, notification service, Booking Management Service

HLD
----

(a) vendor onboarding and profile data flow from vendor (hotel/restro) app -> API_Gateway -> vendor_service (read from cache first, write int db first, once written push the data to message broker as producer) -> vendor_data_cache (redis cluster) -> vendor_db (write master-read slaves SQL cluster) -> message broker (Kafka topic: new_vendor) 

(b) vendor(hotel/restro) search flow from user app -> API_Gateway -> Search Service -> searchdata_cache (redis cluster) -> searchdb (elastic search cluster) -> search consumer pulls new vendors(hotels/restros) from message broker to precompute search index on available vendors-> message broker (kafka topic: new_vendor)

(c) User onboarding and profile data flow from user app -> API_Gateway -> Userservice (read from cache first, write int db first) -> userdata_cache (redis cluster) -> userdb (write master- read slaves cluster)

(d) booking confirmation flow from user app -> API_Gateway -> Booking Service (if desired quanity of rooms/tables are available for specific restaturant and specific datetime then mark booking as BLOCKED in bookingdata_db and send sync requests waiting for payment to finish, if payment callback is successfull, marks booking as CONFIRMED in bookingdata_db and push this data into message broker)-> Payment Service (confirms payment success/failure to booking service)-> bookingdata_cache (redis cluster) -> bookingdata_db (write master- read slaves cluster) -> message broker (Kafka topic: new_booking) -> notification service (consumes new bookng data and send notification to users)

(e) booking cancelled/availed flow from user app -> API_Gateway -> Booking Service (marks booking data as CANCELLED or AVAILED in DB and push this data to message broker as producer) -> bookingdata_cache (redis cluster) -> bookingdata_db (write master- read slaves cluster) -> message broker (Kafka topic: booking_availed, booking_cancelled) -> Archive Service (consumes availed/cancelled booking data and pushes this to archive_db)-> archive_db (cassandra cluster)

(f) see current and past bookings data flow from user app and vendor(hotel/restro) app both -> API_Gateway -> Booking Management service (read from bookingdata_cache for current booking and read from archive_db for past bookings) 


LLD
----

(a) Entity Relationship

user:booking::1:n

city:vendor::1:n

vendor:booking::1:n

vendor:vendor_seat::1:n

vendor:vendor_datetimeslot::1:n

vendor_seat:vendor_datetimeslot::n:n (via bookable_seat_slot)

booking:bookable_seat_slot::1:n


(b) API

POST /user/create

POST /user/login

GET /user/:id

PUT /user/:id

POST /vendor/create

POST /vendor/login

GET /vendors

GET /vendor/:id

PUT /vendor/:id

GET /bookings/vendor/:vendorid

POST /booking/vendor/:vendorid

GET /booking/:bookingid

GET /booking/:bookingid/status

PUT /booking/:bookingid

PUT /booking/:bookingid/status

GET /bookings/user/:userid









