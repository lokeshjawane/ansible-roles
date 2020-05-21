from argparse import ArgumentParser
import os
import sys
import json
import yaml

from google.oauth2 import service_account
import googleapiclient.discovery


# [START iam_get_policy]
def get_policy(project_id):
    """Gets IAM policy for a project."""
    # project_number='1094494279329'

    parser = ArgumentParser()
    parser.add_argument('--file', help="binding file path name")
    parser.add_argument('--project-number', help="GCP project number. checkout project homepage for the same")
    args = parser.parse_args()

    with open(args.file) as ansible_iam_binding:
        data1 = json.load(ansible_iam_binding)

    credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
        scopes=['https://www.googleapis.com/auth/cloud-platform'])
    service = googleapiclient.discovery.build(
        'cloudresourcemanager', 'v1', credentials=credentials)
    data = service.projects().getIamPolicy(
        resource=project_id, body={}).execute()

    data.pop("version")
    data.pop("etag")
    for index1,iam_binding in enumerate(data["bindings"],start=0):
        i = 0
        while i <= len(iam_binding["members"]) - 1:
            member = iam_binding["members"][i]
            if args.project_number in member or iam_binding["role"] == "roles/owner":
                i += 1
            else:
                for x in data1["bindings"]:
                    if x.keys()[0] == iam_binding["role"]:
                        if member in x.values()[0]:
                            member_status=True
                            i += 1
                            break
                        else:
                            member_status = False
                            i -= 1
                    else:
                        member_status = False

                if member_status == False:
                    if i < 0:
                        i = 0
                    data["bindings"][index1]["members"].remove(member)
    return data

def updateIamBindings(project_id):
    existing_iam_bindings=get_policy(project_id)

    parser = ArgumentParser()
    parser.add_argument('--file', help="binding file path name")
    parser.add_argument('--project-number', help="GCP project number. checkout project homepage for the same")
    args = parser.parse_args()

    with open(args.file) as ansible_iam_binding:
        new_iam_binding = json.load(ansible_iam_binding)
    for user in new_iam_binding["bindings"]:
        # print(user)
        for bind_index,role_binding in enumerate(existing_iam_bindings["bindings"],start=0):
            role_status = "false"
            if role_binding["role"] == "roles/owner":
                role_status = "true"
            if role_binding["role"] == user.keys()[0]:
                existing_iam_bindings["bindings"][bind_index]["members"].extend(user.values()[0])
                temp_list=list(dict.fromkeys(existing_iam_bindings["bindings"][bind_index]["members"]))
                existing_iam_bindings["bindings"][bind_index]["members"][:] = []
                existing_iam_bindings["bindings"][bind_index]["members"].extend(temp_list)
                role_status = "true"
                break

        if role_status == "false":
            existing_iam_bindings["bindings"].append({"role" : user.keys()[0], "members" : user.values()[0]})

    credentials = service_account.Credentials.from_service_account_file(filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'], scopes=['https://www.googleapis.com/auth/cloud-platform'])
    service = googleapiclient.discovery.build('cloudresourcemanager', 'v1', credentials=credentials)
    policy = service.projects().setIamPolicy(resource=project_id, body={'policy': existing_iam_bindings}).execute()
    print(policy)
    return policy
    # print("##############################################")
    # print(json.dumps(existing_iam_bindings))

if __name__ == '__main__':
    updateIamBindings(os.environ['GCP_PROJ_ID'])
