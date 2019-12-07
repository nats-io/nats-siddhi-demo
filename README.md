# Using NATS NATS and Siddhi for Stream Processing

The [Siddhi.io](https://siddhi.io) team and [NATS](https://nats.io) team have
collaborated to create this demonstration using NATS JetStream with Siddhi
to provide a high performance, highly scalable stream processing solution.

## Overview

A stream of simulated system data is published into NATS and processed by Siddhi.

TODO:  Provide details

## Filters and Alerts

TODO, describe Siddhi filters, alerts etc on the system data and expected
behavior

## Getting Started

### Dependencies

* [Kubernetes](https://kubernetes.io/)
* [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
* [Siddhi Operator](https://github.com/siddhi-io/siddhi-operator/releases/download/v0.2.1/01-siddhi-operator.yaml)
* [Siddhi Dependencies](https://github.com/siddhi-io/siddhi-operator/releases/download/v0.2.1/00-prereqs.yaml)

### Installation

#### NATS

To install NATS and the streaming server, use the one line NATS Kubernetes
install found in the [nats.k8s](https://github.com/nats-io/k8s) repository.

This will install NATS, NATS Streaming, and NATS Surveyor to monitor the
NATS deployment.

#### Siddhi

Follow the Siddhi [instructions](https://siddhi.io/en/v5.1/docs/siddhi-as-a-kubernetes-microservice/#siddhi-51-as-a-kubernetes-microservice) to install Siddhi as a microservice
into your Kubernetes cluster.

#### Test Applications

TODO

## Running the demonstration

To run the demonstration...

TODO

## TODO

* [ ] Configure the Siddhi Microservice to use the NATS service
* [ ] Generate/Save Test Data
* [ ] Create Test applications and dockerize
