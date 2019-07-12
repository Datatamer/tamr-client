from tamr_unify_client.models.base_resource import BaseResource


class Taxonomy(BaseResource):
    """A project's taxonomy"""

    @classmethod
    def from_json(cls, client, data, api_path):
        return super().from_data(client, data, api_path)
