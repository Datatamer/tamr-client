from tamr_client._types import (
    GoldenRecordsProject,
    JsonDict,
    URL,
)


def _from_json(url: URL, data: JsonDict) -> GoldenRecordsProject:
    """Make golden records project from JSON data (deserialize)

    Args:
        url: Project URL
        data: Project JSON data from Tamr server
    """
    return GoldenRecordsProject(
        url, name=data["name"], description=data.get("description")
    )
