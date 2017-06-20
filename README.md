# Openstack Heat Template Examples

This repository includes some infrastructure automation definitions written by Heat for Openstack. 

<h1>ELK Stack

First example is about creating and extending elastic search cluster with following features;

<h2> 1. provision_ha_elk_cluster.yaml
It creates ELK cluster with
3 elastic masters,
3 elastic data,
2 elastic ingest nodes, 
1 logstash and 1 kibana servers.
Before creating this stack, make sure that project has,
It's own router, internal and external network, 
Key-pair, 
OS image (tested on RHEL7, CentOS7 should be OK too), 
Security group (ingress port tcp 5601 for kibana, desired port for logstash, tcp 9200 and 9300 for elastic)
Accessible NFS server that holds most recent elastic search, kibana and logstash tarballs.
OS should have jdk for Elastic and Logstash, so it can be added into tarballs.
logstash.conf and license.json file should be placed in NFS server.

No need to allocate Floating IP, yaml allocates while creating stack.

2. add_elastic_data_node.yaml
Creates new elastic data node and adds it behind  Openstack elastic-data LB that previously created with "provision_ha_elk_cluster.yaml", so Elastic data cluster scales out.

3. add_elastic_ingest_node.yaml
Creates new elastic ingest node and adds it behind  Openstack elastic-ingest LB that previously created with "provision_ha_elk_cluster.yaml", so Elastic ingest cluster scales out.

4. add_kibana.yaml
Creates new Kibana node. Cloud-init service configures Kibana, Openstack elastic-ingest LB IP is added to Kibana configuration. It visualize by getting data from  Openstack elastic-ingest LB, not reaching directly to ingest node(s), so probablity of losing connection to Elastic Search cluster due to the failure of ingest node(s) that feeds kibana is eleminated.

4. add_logstash.yaml
Creates new Logstash node. Cloud-init service configures Logstash, Openstack elastic-data LB IP is added to Logstash configuration. It sends data to  Openstack elastic-data LB, not directly to data node(s), so probablity of losing connection to Elastic Search cluster due to the failure of data node(s) that configured in Logstash is eleminated.





