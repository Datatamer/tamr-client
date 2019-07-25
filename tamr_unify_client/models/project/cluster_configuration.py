from tamr_unify_client.base_resource import BaseResource


class PublishedClustersConfiguration(BaseResource):
    """
    The configuration of published clusters in a project.

    See https://docs.tamr.com/reference#the-published-clusters-configuration-object
    """

    @classmethod
    def from_json(cls, client, data, api_path):
        return super().from_data(client, data, api_path)

    @property
    def relative_id(self):
        """:type: str"""
        # api_path is alias when it exists, and relative_id when it does not.
        # this distinction is useful for things like refreshing a unified dataset,
        # where using the relative_id would hit
        #   /datasets/{id}:refresh
        # rather than
        #   /projects/{id}/unifiedDataset:refresh.
        # Since cluster configurations don't currently have that kind of aliasing,
        # using api_path is always correct.
        # If configurations ever get aliased, this will need to be updated.
        # This is confusing; there's an RFC for suggestions to improve this
        # #64 https://github.com/Datatamer/unify-client-python/issues/64
        # "Conflation between 'api_path', 'relative_id' / 'relativeId', and
        # BaseResource ctor 'alias'"
        return self.api_path

    @property
    def versions_time_to_live(self):
        """:type: str"""
        return self._data.get("versionsTimeToLive")

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"relative_id={self.relative_id!r}, "
            f"versions_time_to_live={self.versions_time_to_live!r})"
        )
