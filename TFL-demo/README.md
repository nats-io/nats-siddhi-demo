# Bus Delay Analysis 

## Use Case 

Analyse bus delays on each bus stop for a given bus route.

### Init Data 

For a given bus route, all the stops are retrieved, and for each stop, bus arrival timetable is retrieved and stored in an in memory data store.

### Realtime Data

Periodically bus expected bus arrival times are retrieved and published for analysis. 

### Analysis

Check the arrival time with the timetable of the corresponding on route number and stop ID, and determine the bus in on-time or delayed.   

### URLs to retrieve data

**URL Templates Used to Retrieve TFL Data** 

Bus stops: https://api.tfl.gov.uk/line/{{routeNo}}/stoppoints
Timetable : https://api.tfl.gov.uk/line/{{routeNo}}/timetable/{{stopId}}
Realtime bus arrival times: https://api.tfl.gov.uk/line/{{routeNo}}/arrivals

**Sample**

Bus stops: https://api.tfl.gov.uk/line/24/stoppoints
Timetable : https://api.tfl.gov.uk/line/24/timetable/490000152C
Realtime bus arrival times: https://api.tfl.gov.uk/line/24/arrivals

## Steps to Run in a Local Environment

1. Download [Siddhi runner from this URL](https://github.com/siddhi-io/distribution/releases/download/v5.1.2/siddhi-runner-5.1.2.zip).
1. Extract the zip file and here onwards the path to the extracted Siddhi runner directory we refer to as `<SIDDHI_HOME>`.
1. Set the `EMAIL, RECEIVER_EMAIL,` and `EMAIL_PASSWORD` environmental variables in your local machine.
    - For example use following commands to setup environmental variables in Linux/Mac.
        ```sh
        $ export EMAIL="<YOUR_EMAIL>"
        $ export EMAIL_PASSWORD="<YOUR_EMAIL_PASSWORD>"
        $ export RECEIVER_EMAIL="<RECEIVER_EMAIL>"
        ```
1. Clone this repository. Here onwards we refer to the cloned repository as `<NATS-SIDDHI-DEMO>`.
    ```sh
    $ git clone https://github.com/nats-io/nats-siddhi-demo.git
    ```
1. Put all the Siddhi files in `<NATS-SIDDHI-DEMO>/TFL-demo/local-deployment/` to the `<SIDDHI_HOME>/wso2/runner/deployment/siddhi-files/` directory.
1. [Optional] If you need to enable Prometheus monitoring of Siddhi apps, add the following YAML configurations in the `<SIDDHI_HOME>/conf/runner/deployment.yaml`. It will start a server in the `9005` port to send events to Prometheus.
    ```yaml
    metrics:
      enabled: true

    metrics.prometheus:
      reporting:
        prometheus:
          - name: prometheus
            enabled: true
            serverURL: "http://0.0.0.0:9005"
    ```
1. Starts the runner using following command.
    ```sh
    $ sh <SIDDHI_HOME>/bin/runner.sh
    ```
1. Use following cURL commands to starts the apps and trigger the process.
    ```sh
    $ curl --location --request POST 'http://0.0.0.0:8011/arrival' \
    --header 'Content-Type: application/json' \
    --data-raw '{
    "routeNo": "24"
    }'
    ```
1. [Optional] Now if you need to monitor these apps in prometheus, follow these steps.
    1. Create a YAML configuration file `prometheus.yaml` using following configs.
        ```yaml
        # my global config
        global:
          scrape_interval:     15s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
          evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.
          # scrape_timeout is set to the global default (10s).

        # Alertmanager configuration
        alerting:
          alertmanagers:
          - static_configs:
            - targets:
              # - alertmanager:9093

        # Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
        rule_files:
          # - "first_rules.yml"
          # - "second_rules.yml"

        # A scrape configuration containing exactly one endpoint to scrape:
        # Here it's Prometheus itself.
        scrape_configs:
          # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
          - job_name: 'prometheus'

            # metrics_path defaults to '/metrics'
            # scheme defaults to 'http'.
            static_configs:
            - targets: ['localhost:9090']

          - job_name: 'PrometheusReporter'
            scrape_interval: "15s"
            static_configs:
              - targets: ['host.docker.internal:9005']
        ```
    1. Start a prometheus docker.
        ```sh
        $ docker run \
            -p 9006:9090 \
            -v <LOCAL_PATH_TO_PROMETHEUS_YAML>prometheus.yaml:/etc/prometheus/prometheus.yml \
            prom/prometheus
        ```
    1. Now prometheus and Siddhi runner are connected. You can access promentheus server using `http://0.0.0.0:9006/` and execute queries such as `jvm_memory_heap_usage` and monitor the Siddhi apps.

## Steps to Run in a Kubernetes Environment

1. Start a K8s cluster
    - For example minikube:
        ```sh
        $ minikube start --memory 4096 --cpus=4
        ```
1. Enable Ingress
    - Minikube
        ```sh
        $ minikube addons enable ingress
        ```
    - Docker for mac
        ```sh
        $ kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/nginx-0.27.1/deploy/static/mandatory.yaml

        $ kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/nginx-0.27.1/deploy/static/provider/cloud-generic.yaml

        ```
1. Install NATS and NATS streaming operators
    - For K8s version v1.16+ (inclusive)
        ```sh
        $ kubectl apply -f https://github.com/nats-io/nats-operator/releases/download/v0.6.0/00-prereqs.yaml
        $ kubectl apply -f https://github.com/nats-io/nats-operator/releases/download/v0.6.0/10-deployment.yaml
        
        $ kubectl apply -f https://github.com/nats-io/nats-streaming-operator/releases/download/v0.3.0/default-rbac.yaml
        $ kubectl apply -f https://github.com/nats-io/nats-streaming-operator/releases/download/v0.3.0/deployment.yaml
        ```

    - For K8s version < v1.16
        ```sh
        $ kubectl apply -f https://github.com/nats-io/nats-operator/releases/download/v0.6.0/00-prereqs.yaml
        $ kubectl apply -f https://github.com/nats-io/nats-operator/releases/download/v0.6.0/10-deployment.yaml

        $ kubectl apply -f https://github.com/nats-io/nats-streaming-operator/releases/download/v0.2.2/default-rbac.yaml
        $ kubectl apply -f https://github.com/nats-io/nats-streaming-operator/releases/download/v0.2.2/deployment.yaml
        ```

1. Install Siddhi Operator
    ```sh
    $ kubectl apply -f https://github.com/siddhi-io/siddhi-operator/releases/download/v0.2.2/00-prereqs.yaml
    $ kubectl apply -f https://github.com/siddhi-io/siddhi-operator/releases/download/v0.2.2/01-siddhi-operator.yaml
    ```
1. Set the `EMAIL, RECEIVER_EMAIL,` and `EMAIL_PASSWORD` environmental variables values in the `siddhi-process.yaml` file before the deployment using appropriate values.
1. Install the Siddhi Process CR
    ```sh
    $ kubectl apply -f siddhi-process.yaml
    ```

1. Send events to trigger the process

    ```sh
    curl --location --request POST 'http://siddhi/natsdemo-2/8011/arrival' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "routeNo": "24"
    }'
    ```
1. [Optional] Now if you need to monitor these apps in prometheus, follow these steps.
    1. Create a YAML configuration file `prometheus.yaml` using following configs.
        ```yaml
        # my global config
        global:
          scrape_interval:     15s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
          evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.
          # scrape_timeout is set to the global default (10s).

        # Alertmanager configuration
        alerting:
          alertmanagers:
          - static_configs:
            - targets:
              # - alertmanager:9093

        # Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
        rule_files:
          # - "first_rules.yml"
          # - "second_rules.yml"

        # A scrape configuration containing exactly one endpoint to scrape:
        # Here it's Prometheus itself.
        scrape_configs:
          # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
          - job_name: 'prometheus'

            # metrics_path defaults to '/metrics'
            # scheme defaults to 'http'.
            static_configs:
            - targets: ['localhost:9090']

          - job_name: 'PrometheusReporter'
            scrape_interval: "15s"
            static_configs:
              - targets: ['0.0.0.0:9005']
        ```
    1. Use Kubernetes port forwarding to expose the `9005` port in the deployment that you need to monitor.
        ```sh
        $ kubectl port-forward deployment/natsdemo-1-0-8-2 9005:9005
        ```
    1. Start a prometheus docker.
        ```sh
        $ docker run \
            -p 9006:9090 \
            -v <LOCAL_PATH_TO_PROMETHEUS_YAML>prometheus.yaml:/etc/prometheus/prometheus.yml \
            prom/prometheus
        ```
    1. Now prometheus and Siddhi runner are connected. You can access promentheus server using `http://0.0.0.0:9006/` and execute queries such as `jvm_memory_heap_usage` and monitor the Siddhi apps.

## About Apps

## Load Bus Time Schedule App

This app triggers the process by reading an external hosted CSV file and then calls the following APIs to receive bus schedule information.
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
