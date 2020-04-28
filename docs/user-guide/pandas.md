# Pandas Workflow

## Connecting To Tamr

Connecting to a Tamr instance:

```python
import os
import pandas as pd
from tamr_unify_client import Client
from tamr_unify_client.auth import UsernamePasswordAuth

username = os.environ['TAMR_USERNAME']
password = os.environ['TAMR_PASSWORD']

auth = UsernamePasswordAuth(username, password)
tamr = Client(auth)
```
## How to load a dataset as a pandas Dataframe

### In Memory

Loading a `dataset` as a pandas `dataframe` is possible via the `from_records()` method that pandas provides. 
An example is shown below:

```python
my_dataset = tamr.datasets.by_name("my_tamr_dataset")
df = pd.DataFrame.from_records(my_dataset.records())
```

This will construct a pandas dataframe based on the records that are streamed in, and stored in the pandas dataframe.
Once all records have been loaded, you will be able to interact with the dataframe normally. 

Note that as values are typically represented inside `arrays` within Tamr, the values will be encapsulated `lists` 
inside the dataframe. You can use traditional methods in pandas to deal with this; for example `.explode()`. 

### Streaming


#### Custom Generators
In order to customise the data loaded into the pandas dataframe, you can customise the generator object (`dataset.records()`)
that is read into pandas. 

For example, it is possible to automatically flatten all lists with a length of one, and apply this to the `dataset.records()`
generator as follows:

```python
def unlist(lst):
    """
    If object is a list of length one, return first element. 
    Otherwise, return original object. 
    """
    if isinstance(lst, list) and len(lst) is 1:
        return lst[0]
    else:
        return lst

def dataset_to_pandas(dataset):
    """
    Incorporates basic unlisting for easy transfer between Tamr and Pandas. 
    """ 
    for record in dataset.records():
        for key in record:
            record[key] = unlist(record[key])
        yield record

df = pd.DataFrame.from_records(dataset_to_pandas(my_dataset))
```

Similarly, if you only require certain attributes to be loaded, you could customise as follows:

```python
def filter_dataset_to_pandas(dataset, colnames):
    """
    Filter the dataset to only the columns specified as a list in colnames. Note: To upsert the records you need your 
    dataset's primary key. This snippet will always load the primary key if it wasn't provided.
    """
    assert isinstance(colnames, list)
    colnames = dataset.key_attribute_names + colnames if dataset.key_attribute_names[0] not in colnames else colnames
    for record in dataset.records():
        yield {k: unlist(v) for k, v in record.items() if k in colnames}

df = pd.DataFrame.from_records(filter_dataset_to_pandas(dataset, ['City', 'new_attr']))
```