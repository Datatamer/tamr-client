from dataclasses import dataclass, replace
from typing import Tuple

from requests import Session

import tamr_client as tc


@dataclass(frozen=True)
class Dataset:
    url: tc.URL
    key_attribute_names: Tuple[str, ...]


def attributes(session: Session, dataset: Dataset) -> Tuple["tc.Attribute", ...]:
    """Get attributes for this dataset

    Args:
        dataset: Dataset containing the desired attributes

    Returns:
        The attributes for the specified dataset

    Raises:
        requests.HTTPError: If an HTTP error is encountered.
    """
    attrs_url = replace(dataset.url, path=dataset.url.path + "/attributes")
    r = session.get(str(attrs_url))
    attrs_json = tc.response.successful(r).json()

    attrs = []
    for attr_json in attrs_json:
        id = attr_json["name"]
        attr_url = replace(attrs_url, path=attrs_url.path + f"/{id}")
        attr = tc.attribute._from_json(attr_url, attr_json)
        attrs.append(attr)
    return tuple(attrs)
