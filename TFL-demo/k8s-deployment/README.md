This is the YAML artifact that can be used to deploy this solution in a Kubernetes environment.

## Steps to Run

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
    curl --location --request POST 'http://siddhi/natsdemo-0/8012/route' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "routeNo": "24"
    }'

    curl --location --request POST 'http://siddhi/natsdemo-4/8011/arrival' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "routeNo": "24"
    }'
    ```
