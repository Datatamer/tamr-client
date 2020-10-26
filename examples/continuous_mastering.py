from getpass import getpass

import tamr_client as tc

username = input("Tamr Username:")
password = getpass("Tamr Password:")

auth = tc.UsernamePasswordAuth(username, password)
session = tc.session.from_auth(auth)

protocol = "http"
host = "localhost"
port = 9100

instance = tc.Instance(protocol=protocol, host=host, port=port)

project = tc.project.by_name(session, instance, "MasteringTutorial")

if not isinstance(project, tc.MasteringProject):
    raise RuntimeError(f"{project.name} is not a mastering project.")

operation_1 = tc.mastering.update_unified_dataset(session, project)
tc.operation.check(session, operation_1)

operation_2 = tc.mastering.generate_pairs(session, project)
tc.operation.check(session, operation_2)

operation_3 = tc.mastering.apply_feedback(session, project)
tc.operation.check(session, operation_3)

operation_4 = tc.mastering.update_pair_results(session, project)
tc.operation.check(session, operation_4)

operation_5 = tc.mastering.update_high_impact_pairs(session, project)
tc.operation.check(session, operation_5)

operation_6 = tc.mastering.update_cluster_results(session, project)
tc.operation.check(session, operation_6)

operation_7 = tc.mastering.publish_clusters(session, project)
tc.operation.check(session, operation_7)
