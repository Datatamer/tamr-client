
import os

os.environ.setdefault("TAMR_CLIENT_BETA", "1")

import tamr_client as tc

auth = tc.UsernamePasswordAuth('admin', 'dt')
session = tc.session.from_auth(auth)
instance = tc.instance.Instance(host="procurify-demo.tamrdev.com", port=9100)

project = tc.project.from_resource_id(session, instance, "2")

tx = tc.project.transformations(session, project)
print(tx)

dataset = tc.dataset.from_resource_id(session, instance, '3')
new_input_tx = tc.InputTransformation("SELECT *, upper(name) as name;", [dataset])
all_tx = tc.Transformations(input_scope=[new_input_tx], unified_scope=["SELECT *, 1 as one;"])
tc.project.replace_transformations(session, project, all_tx)



