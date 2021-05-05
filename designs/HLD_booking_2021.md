Functional requirements: hotel(restro) onboarding, hotel(restro) manager can see bookings, User can search & filter hotel(restro) for given facility(cuisine) along with location and datetime, user can book/cancel/update room(table) for specific capacity for specific datetime slot, charge users for booking to reduce no-shows and refund same post billing

Non functional requirements: Low latency, High availability, Row level locks to avoid race condition while blocking the slot

Scale: 500k hotels(restro), 10M rooms(tables), 

Services: User service, Vendor(hotel/restro) service, Booking service, search service, payment service, notification service, Booking Management Service

HLD
----

(a) User onboarding and profile data flow from user app -> LB1 -> Userservice (read from cache first, write int db first) -> userdata_cache (redis cluster) -> userdb (write master- read slaves cluster)

(b) vendor onboarding and profile data flow from vendor (hotel/restro) app -> LB2 -> vendor_service (read from cache first, write int db first, once written push the data to message broker as producer) -> vendor_data_cache (redis cluster) -> vendor_db (write master- read slaves cluster) -> message broker (Kafka topic: new_vendor) 

(c) vendor(hotel/restro) search flow from user app -> LB3 -> Search Service -> searchdata_cache (redis cluster) -> searchdb (elastic search cluster) -> search consumer pulls new vendors(hotels/restros) and updated booking data from message broker -> message broker (kafka topic: new_vendor, new_booking)

(d) booking confirmation flow from user app -> LB4 -> Booking Service (if desired quanity of rooms/tables are available for specific restaturant and specific datetime then mark booking as BLOCKED in bookingdata_db and send sync requests waiting for payment to finish, if payment callback is successfull, marks booking as CONFIRMED in bookingdata_db and push this data into message broker)-> Payment Service (confirms payment success/failure to booking service)-> bookingdata_cache (redis cluster) -> bookingdata_db (write master- read slaves cluster) -> message broker (Kafka topic: new_booking) -> notification service (consumes new bookng data and send notification to users)

(e) booking cancelled/availed flow from user app -> LB4 -> Booking Service (marks booking data as CANCELLED or AVAILED in DB and push this data to message broker as producer) -> bookingdata_cache (redis cluster) -> bookingdata_db (write master- read slaves cluster) -> message broker (Kafka topic: booking_availed, booking_cancelled) -> Archive Service (consumes availed/cancelled booking data and pushes this to archive_db)-> archive_db (cassandra cluster)

(f) see current and past bookings data flow from user app and vendor(hotel/restro) app both -> LB5 -> Booking Management service (read from bookingdata_cache for current booking and read from archive_db for past bookings) 
