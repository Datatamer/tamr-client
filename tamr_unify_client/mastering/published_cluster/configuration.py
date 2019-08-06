import copy

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


class PublishedClustersConfigurationBuilder:
    """A builder object to modify an existing published cluster configuration.

    :param cluster_configuration: The cluster configuration to modify.
    :type cluster_configuration: :class:`~tamr_unify_client.mastering.published_cluster.configuration.PublishedClustersConfiguration`
    """

    def __init__(self, cluster_configuration):
        self._data = copy.deepcopy(cluster_configuration._data)
        self.client = cluster_configuration.client
        self.api_path = cluster_configuration.api_path

    def with_versions_time_to_live(self, new_versions_time_to_live):
        """Modifies the configuration's versions time to live.

        :param new_versions_time_to_live: The new versions time to live.
        :type new_versions_time_to_live: str
        :return: The updated builder.
        :rtype: :class:`~tamr_unify_client.mastering.published_cluster.configuration.PublishedClustersConfigurationBuilder`
        """
        self._data["versionsTimeToLive"] = new_versions_time_to_live
        return self

    def put(self):
        """Uploads the new configuration to Unify.

        :return: The updated published cluster configuration.
        :rtype: :class:`~tamr_unify_client.mastering.published_cluster.configuration.PublishedClustersConfiguration`
        """
        new_data = self.client.put(self.api_path, json=self._data).successful().json()
        return PublishedClustersConfiguration.from_json(
            self.client, new_data, self.api_path
        )

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"relative_id={self.api_path!r}, "
            f"versions_time_to_live={self._data['versionsTimeToLive']})"
        )
