Functional requirements:
vendor (hotel/restro) onboarding.
vendor info can be updated in system.
vendor (hotel/restro) manager can view bookings.
User Onboarding.
Users can search & filter vendors (hotel/restro) for given criteria (roomtype/cuisine) along with location and datetime.
users can book/view/cancel/update their bookings (room/table) for specific capacity for specific datetime slot.
vendor can charge users for booking to reduce no-shows and refund same post billing.

Non functional requirements: 
Low latency. High availability.

Booking status = {reserved, confirmed, completed, cancelled}

Here, Reserved means a locked booking where payment is in progress, once payment is done status would be confirmed else cancelled. completed means booking was utilised successfully by the user.

Concurrency: rather using lock on row we would decrement(reserved/confirmed) and increment(completed/cancelled) available itenery in the table  

Choice of DB (Sql v/s Nosql):

PACELC: In case of network partition choose between Availablity & Consistence else choose between Latancy and Consistency
postgres -> PCEC system (strong consistency, Synchronous replication) -> Cant afford stale reads
cassendra -> PAEL system (strong availability, Asynchronous replication) -> Can afford stale reads
Mongodb -> PAEC system (strong availability, Synchronous replication) -> Cant afford stale reads unless there is netwrodk partition

Scale:
500k vendors(hotels/restros)
10M iteneries(rooms/tables) 

Out of scope: Analytics 

Services: User service, Vendor(hotel/restro) service, Active_Booking_service, search service, payment service, notification service, Booking Management Service, archieve_Booking_service

HLD
----

(a) vendor onboarding and profile data flow from vendor (hotel/restro) app -> API_Gateway -> vendor_service (no cache, read/write from db only, once written push the data to message broker as producer) -> vendor_db (write master-read slaves SQL cluster) -> message broker (Kafka topic: new_vendor) 

(b) vendor(hotel/restro) search flow from user app -> API_Gateway -> Search Service -> searchdb (elastic search cluster) -> search consumer updates available itenaries (room/table) of the vendors(hotels/restros) by consuming (new_vendor/new_booking/booking_availed/booking_cancelled) messages from message broker. It also precomputes search index on available vendors-> message broker (kafka topic: new_vendor)

(c) User onboarding and profile data flow from user app -> API_Gateway -> Userservice (no cache, read/write from db only) -> userdb (write master- read slaves cluster)

(d) booking confirmation flow from user app -> API_Gateway -> Booking Service (if desired quanity of rooms/tables are available for specific restaturant and specific datetime then mark booking as BLOCKED in bookingdata_db and send sync requests waiting for payment to finish, if payment callback is successfull, marks booking as CONFIRMED in bookingdata_db and push this data into message broker)-> Payment Service (confirms payment success/failure to booking service)-> Active_bookingdata_cache (redis cluster) -> bookingdata_db (write master- read slaves cluster) -> message broker (Kafka topic: new_booking) -> notification service (consumes new bookng data and send notification to users and vendor)

(e) booking cancelled/availed flow from user app -> API_Gateway -> Booking Service (marks booking data as CANCELLED or AVAILED in DB, invalidates cache and push this data to message broker as producer) -> Active_bookingdata_cache (redis cluster) -> bookingdata_db (write master- read slaves cluster) -> message broker (Kafka topic: booking_availed, booking_cancelled) -> notification service (consumes cancelled bookng data and send notification to users) -> Archive Booking Service (consumes availed/cancelled booking data and pushes this to archive_db) -> archive_db (cassandra cluster)

(f) see current and past bookings data flow from user app and vendor(hotel/restro) app both -> API_Gateway -> Booking Management service (read from bookingdata_cache for current booking and read from archive_db for past bookings) 

(g) Analytics -> Spark streaming consumer consumes from kafka and pushes into hadoop cluster


Bonus: Dynamic pricing engine to set prices based on supply demand analytics

LLD
----

(a) Tables 

Tables of vendor_db -> city, vendor(hotel/restro), facility(amenity/offer), itenery(room-type/table-type), itenery_facility(room_amenity/table_offer)

Tables of Booking_db -> vendor_available_itenary(bookable-vendor-room-type/bookable-restro-table-type), vendor_datetimeslot, active_booking (reserved/confirmed booking), inactive_booking (completed/cancelled booking). 



(b) Entity Relationship

user:booking::1:n

city:vendor::1:n

vendor:booking::1:n

vendor:vendor_available_itenary::1:n

vendor:vendor_datetimeslot::1:n

vendor_available_itenary:vendor_datetimeslot::n:n (via vendor_available_itenary_datetimeslot)

  -> vendor_available_itenary_datetimeslot:vendor_available_itenary::1:n
  
  -> vendor_available_itenary_datetimeslot:vendor_datetimeslot::1:n

booking:vendor_available_itenary_datetimeslot::1:n


(c) API

POST /user/create

POST /user/login

GET /user/:userid

PUT /user/:userid

POST /vendor/create

POST /vendor/login

GET /vendors

GET /vendor/:vendorid

PUT /vendor/:vendorid

PUT /vendor/:vendorid/itenery/:iteneryid

GET /bookings/vendor/:vendorid

POST /booking/vendor/:vendorid

GET /booking/:bookingid

GET /booking/:bookingid/status

PUT /booking/:bookingid

PUT /booking/:bookingid/status

GET /bookings/user/:userid









