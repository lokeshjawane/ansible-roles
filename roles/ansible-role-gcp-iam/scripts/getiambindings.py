#!/usr/bin/env python

import simplejson
import sys
import yaml
import json

gcp_iam_bindings=[]

for x in json.loads(sys.stdin.read())["bindings"]:
    gcp_iam_bindings.append({x["role"]:x["members"]})

print yaml.dump(simplejson.loads(json.dumps(gcp_iam_bindings)), default_flow_style=False)
