# openstack

This repository includes some infrastructure automation definitions written by Heat for Openstack. 

ELK Stack

First example is about creating and extending elastic search cluster with following features;

1. provision_ha_elk_cluster.yaml
It creates ELK cluster with
3 elastic masters,
3 elastic data,
2 elastic ingest nodes, 
1 logstash and 1 kibana servers.
Before creating this stack, make sure that project has,
It's own router, internal and external network, 
Key-pair, 
OS image (tested on RHEL7, CentOS7 should be OK too), 
Security group (ingress port tcp 5601 for kibana, desired port for logstash should be added for external communication, elastic port 9200 is not mandatory)
Accessible NFS server that holds most recent elastic search, kibana and logstash tarballs.
OS should have jdk for Elastic and Logstash, so it can be added into tarballs. 

No need to allocate Floating IP, yaml allocates while creating stack.

2. add_elastic_data_node.yaml
Creates new elastic data node and adds it behind elastic-data Openstack LB that previously created with "provision_ha_elk_cluster.yaml", so Elastic data cluster scales out.

3. add_elastic_ingest_node.yaml
Creates new elastic ingest node and adds it behind elastic-ingest Openstack LB that previously created with "provision_ha_elk_cluster.yaml", so Elastic ingest cluster scales out.

4. add_kibana.yaml
Creates new kibana node. Cloud-init service configures kibana, elastic-ingest Openstack LB is added to kibana configuration.
It visualize by getting data from elastic-ingest Openstack LB, not reaching directly to ingest nodes, so 


