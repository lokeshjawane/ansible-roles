ansible-role-gcp-iam
=========

This ansible help you to manage the IAM user access to GCP project. You can integrate this role to CI/CD pipeline or any other automation process to manage IAM user access.


Requirements
------------

Make sure listed python packages(pip) are installed
```
google-api-python-client==1.7.11
google-auth==1.6.3
google-auth-httplib2==0.0.3
```
Role Variables
--------------

|Name |default|Desc|
|--|--|--|
|gcp_iam_bindings| blank| (required) list of hash with role, members keys |
|gcp_project_number|blank|(required)GCP project number. checkout project homepage for the same|
|gcp_project_id|blank|(required)GCP project ID|

Dependencies
------------
N/a


## How To

Eg.
#### 1. Create extra vars.yml file and add bindings for new GCP project.
```
gcp_iam_bindings:
- roles/bigquery.admin:
  - user:abc@com
- roles/cloudfunctions.serviceAgent:
  - serviceAccount:service-1111111111111@gcf-admin-robot.iam.gserviceaccount.com

gcp_project_number: "111111111111"
```
**NOTE**: Make sure you are using `user:*` to add user and `serviceAccount:*` to add service account.

OR

If you wants to manage existing project? then get IAM binding from existing project, update bindings and add to extravars file. Use below command to get the policy.
```
gcloud projects get-iam-policy cc-interview-sandbox --format='json(bindings)'  | python scripts/getiambindings.py
```
It should print O/P something like:
```
- roles/bigquery.admin:
  - user:abc@com
- roles/cloudfunctions.serviceAgent:
  - serviceAccount:service-1111111111111@gcf-admin-robot.iam.gserviceaccount.com
```

#### 2. Run ansible playbook now
```
#create playbook(sites.yml)
- hosts: localhost
  gather_facts: false
  connection: local
  roles:
  - roles/ansible-role-gcp-iam

# Export GOOGLE_APPLICATION_CREDENTIAL with JSON key file for GCP auth
export GOOGLE_APPLICATION_CREDENTIALS=/<path to .json JSON key file>

#Execute playbook
ansible-playbook sites.yml --extra-vars=@vars.yml -v
```


## Limitations:

Granting Owner access to user is not possible with this automation as assigning project owner access send an invite to user. Refer: [https://cloud.google.com/resource-manager/reference/rest/v1beta1/projects/setIamPolicy](https://cloud.google.com/resource-manager/reference/rest/v1beta1/projects/setIamPolicy)
