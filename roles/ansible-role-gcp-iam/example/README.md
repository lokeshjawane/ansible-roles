1. Modify params.yml with binding details, gcp project id and number
2. Export bash var GOOGLE_APPLICATION_CREDENTIALS=<.json file path>
2. Run below command to execute ansible playbook
```
ansible-playbook  sites.yml -e '@params.yml
```
