import requests
import json


def get_token(ip, user, opass, proj, renew):
	
	token_file="token_"+user+"_"+proj
	if renew == 0:
		try:
			file=open(token_file,"r")
			fout=file.readline().split(",")
			token=fout[0]
			proj_id=fout[1]
			file.close()
			print("INFO: Got token from file: "+ token_file)
		except:
			print("INFO: Failed to get token from file, renewing token")
			token, proj_id=get_token(ip, user, opass, proj, 1)
	if renew == 1:
		url = "http://"+ip+":5000/v3/auth/tokens"
		payload = "{ \"auth\": { \"identity\": { \"methods\": [ \"password\" ], \"password\": { \"user\": { \"domain\": { \"name\": \"Default\" }, \"name\": \""+user+"\", \"password\": \""+opass+"\" } } }, \"scope\": { \"project\": { \"domain\": { \"name\": \"Default\" }, \"name\": \""+proj+"\" } } } }"
		headers = {
	    		'content-type': "application/json",
		    	'cache-control': "no-cache",
	        }
		response = requests.request("POST", url, data=payload, headers=headers)
		token=response.headers['X-Subject-Token']
		data_json=response.text
		data=json.loads(data_json)
		if data['token']['project']['name'] == proj:
			proj_id=(data['token']['project']['id'])
		
		file=open(token_file,"w")
		file.write(token+","+proj_id)
		file.close()
		
	return token, proj_id


def printEnvInfo(ip, user, opass, proj):
    token, proj_id=get_token(ip, user, opass, proj, 0)
    get_instances = "http://"+ip+":8774/v2.1/servers/detail"
    get_lbaasinfo = "http://"+ip+":9696/v2.0/lb/pools"
    get_stacks = "http://"+ip+":8004/v1/"+proj_id+"/stacks"    
    headers = {
      'accept': "application/json",
      'x-auth-token': token,
      'cache-control': "no-cache",
    }
    
    instance_response=requests.request("GET", get_instances, headers=headers).status_code
    if instance_response == 401:
       print("INFO: Token got from token file expired, renewing")
       headers['x-auth-token'], proj_id=get_token(ip, user, opass, proj, 1)

    instance_data_json=requests.request("GET", get_instances, headers=headers).text
    instance_data=json.loads(instance_data_json)
    
    stack_data_json=requests.request("GET", get_stacks, headers=headers).text
    stack_data=json.loads(stack_data_json)

    lbaas_data_json=requests.request("GET", get_lbaasinfo, headers=headers).text
    lbaas_data=json.loads(lbaas_data_json)
    
    
    print("OUTPUT: Stacks Information")
    for stack in stack_data['stacks']:
       print("Stack Name: ",stack['stack_name'], "          Stack Link: ",stack['links'][0]['href'])
    
    print("OUTPUT: Instances Information")       
    for server in instance_data['servers']:
       try:
       	print("Instance Name: ", server['name'],"     Internal Ip: ",server['addresses']['int'][0]['addr'], "     Floating Ip: ",server['addresses']['int'][1]['addr'], "     Instance Metadata Type: ",server['metadata']['type'])
       except IndexError:
       	print("Instance Name: ",server['name'],"     Internal Ip: ",server['addresses']['int'][0]['addr'],"                         Instance Metadata Type: ", server['metadata']['type'])
       	
    print ("OUTPUT: Load Balancer Information")
    for lb in lbaas_data['pools']:
        print("LB Name: ", lb['name'], "LB Pool ID: ", lb['id'])


def main():
	openstack_ip=""
    project_user_name=""
    project_user_pass=""
	project_name=""
	printEnvInfo(openstack_ip, project_user_name, project_user_pass, project_name)
	
if __name__ == "__main__":
    main()
	
	
	
	


