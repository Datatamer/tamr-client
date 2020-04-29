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
## Load dataset as Dataframe

### Loading: In Memory

Loading a `dataset` as a pandas `dataframe` is possible via the `from_records()` method that pandas provides. 
An example is shown below:

```python
my_dataset = tamr.datasets.by_name("my_tamr_dataset")
df = pd.DataFrame.from_records(my_dataset.records())
```

This will construct a pandas dataframe based on the records that are streamed in, and stored in the pandas dataframe.
Once all records have been loaded, you will be able to interact with the dataframe normally. 

Note that as values are typically represented inside `arrays` within Tamr, the values will be encapsulated `lists` 
inside the dataframe. You can use traditional methods in pandas to deal with this; for example by calling `.explode()`,
or extracting specific elements. 

### Loading:  Streaming
When working with large `datasets` it is sometimes better not to work in memory, but to iterate through a dataset. 
Since `dataset.records()` is a generator, this can easily be done as follows:
```python
for record in dataset.records():
    df = pd.DataFrame.from_records(record)
``` 

### Custom Generators
In order to customise the data loaded into the pandas dataframe, it is possible to customise the generator object 
`dataset.records()` by wrapping it in a different generator.  

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

Similarly, it is possible to filter to extracting only certain attributes, by specifying this in the generator:

```python
def filter_dataset_to_pandas(dataset, colnames):
    """
    Filter the dataset to only the primary key and the columns specified as a list in colnames. 
    """
    assert isinstance(colnames, list)
    colnames = dataset.key_attribute_names + colnames if dataset.key_attribute_names[0] not in colnames else colnames
    for record in dataset.records():
        yield {k: unlist(v) for k, v in record.items() if k in colnames}

df = pd.DataFrame.from_records(filter_dataset_to_pandas(my_dataset, ['City', 'new_attr']))
```

Note that upserting these records back to the original Tamr Dataset would overwite the existing records and attributes, and cause loss of the data 
stored in the unloaded attributes.  

## Upload Dataframe as Dataset

### Create New Dataset
To create a new dataset and upload data, the convenience function `dataset.create_from_dataframe()` can be used. 
Note that Tamr will throw an error if columns aren't generally formatted as strings. (The exception being geospatial
columns. For that, see the geospatial examples.)

In order to achieve this, the following code will transform the column types to string.
```python
df = df.astype(str)
```

Creating the dataset is as easy as calling:
```python
tamr.datasets.create_from_dataframe(df, 'primaryKey', 'my_new_dataset')
```

### Changing Values

#### Making Changes: In Memory 
When making changes to a dataset that was loaded as a dataframe, changes can be pushed back to Tamr using the 
`dataset.upsert_from_dataframe()` method as follows:

```python
df = pd.DataFrame.from_records(my_dataset.records())
df['column'] = 'new_value'
my_dataset.upsert_from_dataframe(df, primary_key_name='primary_key')
```

#### Making Changes: Streaming
For larger datasets it might be better to stream the data and apply changes while iterating through the dataset. 
This way the full dataset does not need to be loaded into memory. 
```python
for record in dataset.records():
    df = pd.DataFrame.from_records(record)
    df['column_to_change'] = 'new_value'
    dataset.upsert_from_dataframe(df, primary_key_name='primary_key')
```
### Adding Attributes
When making changes to dataframes, new dataframe columns are not automatically created as attributes when upserting 
records to Tamr. In order for these changes to be recorded, these attributes first need to be created. 

One way of creating these for source datasets automatically would be as follows:

```python
def add_missing_attributes(dataset, df):
    """
    Detects any attributes in the dataframe that aren't in the dataset and attempts to add them (as strings).
    """
    existing_attributes = [att.name for att in dataset.attributes]
    new_attributes = [att for att in df.columns.to_list() if att not in existing_attributes]
    
    if not new_attributes:
        return
    
    for new_attribute in new_attributes:
        attr_spec = {"name": new_attribute,
                     "type": {"baseType": "ARRAY", "innerType": {"baseType": "STRING"}},
                    }
        dataset.attributes.create(attr_spec)

add_missing_attributes(my_dataset, df)
```
