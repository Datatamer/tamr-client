Creating and Modifying Resources
================================

Creating resources
------------------

Resources, such as projects, dataset, and attribute configurations,
can be created through their respective collections.
Each ``create`` function takes in a dictionary that conforms to the
`Tamr Public Docs <https://docs.tamr.com/reference>`_ for creating that resource type::

    spec = {
        "name": "project",
        "description": "Mastering Project",
        "type": "DEDUP"
        "unifiedDatasetName": "project_unified_dataset"
    }
    project = tamr.projects.create(spec)

Using specs
-----------

These dictionaries can also be created using spec classes.

Each ``Resource`` has a corresponding ``ResourceSpec`` which can be used to build an
instance of that resource by specifying the value for each property.

The spec can then be converted to a dictionary that can be passed to ``create``.

For instance, to create a project::

    spec = (
        ProjectSpec.new()
        .with_name("Project")
        .with_type("DEDUP")
        .with_description("Mastering Project")
        .with_unified_dataset_name("Project_unified_dataset")
    )
    project = tamr.projects.create(spec.to_dict())


Calling ``with_*`` on a spec creates a new spec with the same properties besides the
modified one. The original spec is unaltered, so it could be used multiple times::

    base_spec = (
        ProjectSpec.new()
        .with_type("DEDUP")
        .with_description("Mastering Project")
    )

    specs = []
    for name in project_names:
        spec = (
            base_spec.with_name(name)
            .with_unified_dataset_name(name + "_unified_dataset")
        )
        specs.append(spec)

    projects = [tamr.projects.create(spec.to_dict()) for spec in specs]


Creating a dataset
------------------

Datasets can be created as described above, but the dataset's schema and
records must then be handled separately.

To combine all of these steps into one, ``DatasetCollection`` has a convenience
function ``create_from_dataframe`` that takes a
`Pandas DataFrame <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_.
This makes it easy to create a Tamr dataset from a CSV::

    import pandas as pd

    df = pd.read_csv("my_data.csv")
    dataset = tamr.datasets.create_from_dataframe(df, "primary key name", "My Data")


This will create a dataset called "My Data" with the specified primary key, an attribute
for each column of the ``DataFrame``, and the ``DataFrame``'s rows as records.

Modifying a resource
--------------------

Certain resources can also be modified using specs.

After getting a spec corresponding to a resource and modifying some properties,
the updated resource can be committed to Unify with the ``put`` function::

    updated_dataset = (
        dataset.spec()
        .with_description("Modified description")
        .put()
    )

Each spec class has many properties that can be changed, but refer to the
`Public Docs <https://docs.tamr.com/reference>`_ for which properties will actually be updated in Tamr.
If an immutable property is changed in the update request, the new value will simply be ignored.
