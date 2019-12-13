#Bus Delay Analysis 

## Use Case 

Analyse bus delays on each bus stop for a given bus route. 

### Init Data 

For a given bus route, all the stops are retrieved, and for each stop, bus arrival timetable is retrieved and stored in an in memory data store. 

### Realtime Data

Periodically bus expected bus arrival times are retrieved and published for analysis. 

### Analysis

Check the arrival time with the timetable of the corresponding on route number and stop ID, and determine the bus in on-time or delayed.   

### URLS to retrieve data

**URLS templates used to retrieve TFL data** 

Bus stops: https://api.tfl.gov.uk/line/{{routeNo}}/stoppoints
Timetable : https://api.tfl.gov.uk/line/{{routeNo}}/timetable/{{stopId}}
Realtime bus arrival times: https://api.tfl.gov.uk/line/{{routeNo}}/arrivals

**Sample**

Bus stops: https://api.tfl.gov.uk/line/24/stoppoints
Timetable : https://api.tfl.gov.uk/line/24/timetable/490000152C
Realtime bus arrival times: https://api.tfl.gov.uk/line/24/arrivals

