# Openstack Heat Template Examples

This repository includes some infrastructure automation definitions written by Heat for Openstack. 

* [ELK Stack](https://github.com/okansahiner/openstack#elk-stack)
* [Cassandra Stack](https://github.com/okansahiner/openstack#cassandra-stack)
* [Wordpress Stack](https://github.com/okansahiner/openstack#wordpress-stack)
* [Sample Stacks](https://github.com/okansahiner/openstack#sample-stacks)


## ELK Stack

![](images/elk_topology.png?raw=true)

First example is about creating and extending elastic search cluster with following features;

#### 1. provision_ha_elk_cluster.yaml
It creates ELK cluster with
* 3 elastic masters,
* 3 elastic data,
* 2 elastic ingest nodes, 
* 1 logstash and 1 kibana servers,
* Openstack LB for EL Data Pool,
* Openstack LB for EL Index Pool.

Before creating this stack, make sure that project has,
* It's own router, internal and external network, 
* Key-pair, 
* OS image (tested on RHEL7, CentOS7 should be OK too), 
* Security group (ingress port tcp 5601 for kibana, desired port for logstash, tcp 9200 and 9300 for elastic)
* Accessible NFS server that holds most recent elastic search, kibana and logstash tarballs.
* OS should have jdk for Elastic and Logstash, so it can be added into tarballs.
* logstash.conf and license.json file should be placed in NFS server.

No need to allocate Floating IP, yaml allocates while creating stack.

#### 2. add_elastic_data_node.yaml
Creates new elastic data node and adds it behind  Openstack elastic-data LB that previously created with "provision_ha_elk_cluster.yaml", so Elastic data cluster scales out.

#### 3. add_elastic_ingest_node.yaml
Creates new elastic ingest node and adds it behind  Openstack elastic-ingest LB that previously created with "provision_ha_elk_cluster.yaml", so Elastic ingest cluster scales out.

#### 4. add_kibana.yaml
Creates new Kibana node. Cloud-init service configures Kibana, Openstack elastic-ingest LB IP is added to Kibana configuration. It visualize by getting data from  Openstack elastic-ingest LB, not reaching directly to ingest node(s), so probablity of losing connection to Elastic Search cluster due to the failure of ingest node(s) that feeds kibana is eleminated.

#### 5. add_logstash.yaml
Creates new Logstash node. Cloud-init service configures Logstash, Openstack elastic-data LB IP is added to Logstash configuration. It sends data to  Openstack elastic-data LB, not directly to data node(s), so probablity of losing connection to Elastic Search cluster due to the failure of data node(s) that configured in Logstash is eleminated.

#### 6. repair_master_node.yaml
Provisions master node in case of master failures. Replaces new master instead of failed one.

## Cassandra Stack

![](images/cassandra_topology.png?raw=true)

This example is about creating and extending Cassandra cluster with following features;

#### 1. provision_cluster.yaml
It creates Cassandra cluster with
* 2 cassandra seeds,
* 2 cassandra nodes,
* Openstack LB for Cassandra instances.

Before creating this stack, make sure that project has,
* It's own router, internal and external network, 
* Key-pair, 
* OS image (tested on RHEL7, CentOS7 should be OK too), 
* Security group (ingress port tcp 9042 for cql , 7000 for internode communication)
* Accessible NFS server that holds most recent Cassandra tarballs.
* OS should have jdk for Cassandra, so it can be added into tarballs.

No need to allocate Floating IP, yaml allocates while creating stack.

#### 2. add_node.yaml
Creates new cassandra node and adds it behind Openstack Cassandra LB that previously created with "provision_cassandra..yaml".

## Wordpress Stack

![](images/wp_topology.png?raw=true)

This example is about creating wordpress stack  with following features;

#### 1. provision_wp.yaml
It creates Wordpress stack with
* 1 Application server instance,
* 1 Database server instance,

Before creating this stack, make sure that project has,
* It's own router, internal and external network, 
* 2 Internal networks can be used for app & db network isolation,
* Key-pair, 
* 2 prepared OS templates , Mysql installed and Apache+PHP+Wordpress installed,  (tested on RHEL7, CentOS7 should be OK too), 
* Security group (ingress port tcp 80,443 and 3306)
* Also, wp_first_install.sh curl script allows to configure Wordpress first initialization.

No need to allocate Floating IP, yaml allocates while creating stack.

## Sample Stacks

This example is about creating some sample stacks with following features;

#### 1. provision_rhel7.yaml
It creates RHEL7 instance with
* key pair,
* floating ip,
* security group,
* time server, name server configuration

Before creating this stack, make sure that project has,
* It's own router, internal and external network, 
* Key-pair, 
* OS image (tested on RHEL7, CentOS7 should be OK too), 
* Security group (ingress port ssh for communication)

No need to allocate Floating IP, yaml allocates while creating stack.

#### 2. provision_LB.yaml

It creates Openstack Load Balancer with following specs,
* Front Port
* Redirect Port
* Floating IP attached to Virtual IP


#### 3. add_member_to_lb.yaml

It creates RHEL7 instance (same specs with provision_rhel7.yaml ) and adds it as a member of previously created  Load Balancer with provision_LB.yaml.







