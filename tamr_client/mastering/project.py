from tamr_client._types import JsonDict, MasteringProject, URL


def _from_json(url: URL, data: JsonDict) -> MasteringProject:
    """Make mastering project from JSON data (deserialize)

    Args:
        url: Project URL
        data: Project JSON data from Tamr server
    """
    return MasteringProject(url, name=data["name"], description=data.get("description"))
