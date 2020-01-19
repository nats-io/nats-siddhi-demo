This set of Siddhi apps implemented to cater to the use case of analyze the bus arrival times and notified users if there is any delay in a given bus route.

## Steps to Run

1. Download [Siddhi runner from this URL](https://github.com/siddhi-io/distribution/releases/download/v5.1.2/siddhi-runner-5.1.2.zip).
1. Extract the zip file and here onwards the path to the extracted Siddhi runner directory we refer to as `<SIDDHI_HOME>`.
1. Set the `EMAIL, RECEIVER_EMAIL,` and `EMAIL_PASSWORD` environmental variables in your local machine.
    - For example use following commands to setup environmental variables in Linux/Mac.
        ```sh
        $ export EMAIL="<YOUR_EMAIL>"
        $ export EMAIL_PASSWORD="<YOUR_EMAIL_PASSWORD>"
        $ export RECEIVER_EMAIL="<RECEIVER_EMAIL>"
        ```

1. Put all the Siddhi files here to the `<SIDDHI_HOME>/wso2/runner/deployment/siddhi-files/` directory.
1. Starts the runner using following command.
    ```sh
    $ sh <SIDDHI_HOME>/bin/runner.sh
    ```
1. Use following cURL commands to starts the apps and trigger the process.
    ```sh
    $ curl --location --request POST 'http://0.0.0.0:8012/route' \
    --header 'Content-Type: application/json' \
    --data-raw '{
    "routeNo": "24"
    }'

    $ curl --location --request POST 'http://0.0.0.0:8011/arrival' \
    --header 'Content-Type: application/json' \
    --data-raw '{
    "routeNo": "24"
    }'
    ```

## About Apps

### Input Route App

This is the app that receives the first cURL request and triggers the process of creating the bus schedule according to the given route.

## Load Bus Time Schedule App

This app calls the following APIs to receive bus schedule information.
- Call `https://api.tfl.gov.uk/line/{{routeNo}}/stoppoints` API to receive stop points of a given route.
- Call `https://api.tfl.gov.uk/line/{{routeNo}}/timetable/{{stopId}}` API to get receive the timetable according to a given route number and a stop ID.

## Arrival Info App

This app calls the `https://api.tfl.gov.uk/line/{{routeNo}}/arrivals` API and time to time receive information related to bus arrivals for a given time.

## Control App

This is the central app that manages the overall process centrally. After the execution of the `InputRoute` and `LoadBusTimeSchedule` apps, we receive a bus time table for a given route. All the process of finding bus arrival information and sending alerts will be starting from this control app. This app triggers the process using the following cURL command.

 ```sh
 $ curl --location --request POST 'http://0.0.0.0:8011/arrival' \
 --header 'Content-Type: application/json' \
 --data-raw '{
 "routeNo": "24"
 }'
 ```

## Late Arrival Analysis App

The main job of this app to analyze the latencies of each bus route. It joins the bus time table with the arrival information stream and finds out latencies. Then it sends all the latencies to the alert stream which responsible for sending alerts to the end-users.

## Delay Alert App

This is the final app responsible for sending alerts to the users.
