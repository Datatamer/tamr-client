# Tutorial: Continuous Mastering
This tutorial will cover using the Python client to keep a Mastering project up-to-date.  This includes carrying new data through to the end of the project and using any new labels to update the machine-learning model.

## Prerequisites
To complete this tutorial you will need:
- `tamr-unify-client` [installed](../../user-guide/installation)
- access to a Tamr instance, specifically:
  - a username and password that allow you to log in to Tamr
  - the socket address of the instance
- an existing Mastering project with loaded data that has been run to the end at least once
  - it is recommended that you first complete the tutorial [here](https://docs.tamr.com/tamr-tutorials/docs/overview-mastering)
  - alternatively, a different Mastering project can be used however the project name will likely be different

## Steps
### Configure the Session and Instance
- Use your username and password to create an instance of `tamr_client.UsernamePasswordAuth`.
- Use the function `tamr_client.session.from.auth` to create a `Session`.
```eval_rst
.. literalinclude:: ../../../examples/continuous_mastering.py
    :language: python
    :lines: 1-9
```
- Create an `Instance` using the `protocol`, `host`, and `port` of your Tamr instance. Replace the values of `protocol`, `host`, and `port` with the corresponding values for your Tamr instance.
```eval_rst
.. literalinclude:: ../../../examples/continuous_mastering.py
    :language: python
    :lines: 11-15
```

### Get the Tamr Mastering project to be updated
Use the function `tc.project.by_name` to retrieve the project information from the server.
```eval_rst
.. literalinclude:: ../../../examples/continuous_mastering.py
    :language: python
    :lines: 17
```
Ensure that the retrieved project is a Mastering project by checking its type:
```eval_rst
.. literalinclude:: ../../../examples/continuous_mastering.py
    :language: python
    :lines: 19-20
```

### Update the unified dataset
To apply the [attribute mapping configuration](https://docs.tamr.com/tamr-tutorials/docs/define-project-schema-mastering) and any transformations to update the unified dataset with updated source data, use the function `tc.mastering.update_unified_dataset`.
```eval_rst
.. literalinclude:: ../../../examples/continuous_mastering.py
    :language: python
    :lines: 22-23
```
This function and all others in this tutorial are *synchronous*, meaning that they will not return until the job in Tamr has resolved, either successfully or unsuccessfully.  The function `tc.operation.check` will raise an exception and halt the script if the job started in Tamr fails for any reason.

### Generate pairs
To generate pairs according to the [configured pair filter rules](https://docs.tamr.com/tamr-tutorials/docs/setup-how-pairs-are-found), use the function `tc.mastering.generate_pairs`
```eval_rst
.. literalinclude:: ../../../examples/continuous_mastering.py
    :language: python
    :lines: 25-26
```

### Train the model with new Labels
To [update the machine-learning model](https://docs.tamr.com/tamr-tutorials/docs/help-tamr-learn-about-your-data) with newly-applied pairs. use the function `tc.mastering.apply_feedback`
```eval_rst
.. literalinclude:: ../../../examples/continuous_mastering.py
    :language: python
    :lines: 28-29
```
Note: The "Apply feedback and update results" action in the Tamr GUI is equivalent to this and the following section.

### Apply the model
Applying the trained machine-learning model requires three functions.
- To update the pair prediction results, use the function `tc.mastering.update_pair_results`
```eval_rst
.. literalinclude:: ../../../examples/continuous_mastering.py
    :language: python
    :lines: 31-32
```
- To update the list of [high-impact pairs](https://docs.tamr.com/tamr-tutorials/docs/help-tamr-learn-about-your-data#4-filter-for-high-impact-pairs), use the function `tc.mastering.update_high_impact_pairs`
```eval_rst
.. literalinclude:: ../../../examples/continuous_mastering.py
    :language: python
    :lines: 34-35
```
- To update the clustering results, use the function `tc.mastering.update_cluster_results`
```eval_rst
.. literalinclude:: ../../../examples/continuous_mastering.py
    :language: python
    :lines: 37-38
```

### Publish the clusters
To publish the record clusters, use the function `tc.mastering.publish_clusters`
```eval_rst
.. literalinclude:: ../../../examples/continuous_mastering.py
    :language: python
    :lines: 40-41
```


All of the above steps can be combined into the following script `continuous_mastering.py`:

```eval_rst
.. literalinclude:: ../../../examples/continuous_mastering.py
    :language: python
```
To run the script via command line:
```bash
TAMR_CLIENT_BETA=1 python continuous_mastering.py
```

To continue learning, see other tutorials and examples.