from copy import deepcopy

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

    def spec(self):
        """Returns a spec representation of this published cluster configuration.

        :return: The published cluster configuration spec.
        :rtype: :class`~tamr_unify_client.mastering.published_cluster.configuration.PublishedClustersConfigurationSpec`
        """
        return PublishedClustersConfigurationSpec.of(self)

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"relative_id={self.relative_id!r}, "
            f"versions_time_to_live={self.versions_time_to_live!r})"
        )


class PublishedClustersConfigurationSpec:
    """A representation of the server view of published clusters configuration."""

    def __init__(self, client, data, api_path):
        self.client = client
        self._data = data
        self.api_path = api_path

    @staticmethod
    def of(resource):
        """Creates an published cluster configuration spec from published cluster configuration.

        :param resource: The existing published cluster configuration.
        :type resource: :class:`~tamr_unify_client.mastering.published_cluster.configuration.PublishedClustersConfiguration`
        :return: The corresponding published cluster configuration spec.
        :rtype: :class:`~tamr_unify_client.mastering.published_cluster.configuration.PublishedClustersConfigurationSpec`
        """
        return PublishedClustersConfigurationSpec(
            resource.client, deepcopy(resource._data), resource.api_path
        )

    def from_data(self, data):
        """Creates a spec with new data.

        :param data: The data for the new spec.
        :type data: dict
        :return: The new spec.
        :rtype: :class:`~tamr_unify_client.mastering.published_cluster.configuration.PublishedClustersConfigurationSpec`
        """
        return PublishedClustersConfigurationSpec(self.client, data, self.api_path)

    def to_dict(self):
        """Returns a version of this spec that conforms to the API representation.

        :returns: The spec's dict.
        :rtype: dict
        """
        return deepcopy(self._data)

    def with_versions_time_to_live(self, new_versions_time_to_live):
        """Creates a new spec with the same properties, updating versions time to live.

        :param new_versions_time_to_live: The new versions time to live.
        :type new_versions_time_to_live: str
        :return: A new spec.
        :rtype: :class:`~tamr_unify_client.mastering.published_cluster.configuration.PublishedClustersConfigurationSpec`
        """
        return self.from_data(
            {**self._data, "versionsTimeToLive": new_versions_time_to_live}
        )

    def put(self):
        """Commits these changes by updating the configuration in Tamr.

        :return: The updated configuration.
        :rtype: :class:`~tamr_unify_client.mastering.published_cluster.configuration.PublishedClustersConfiguration`
        """
        updated_json = (
            self.client.put(self.api_path, json=self._data).successful().json()
        )
        return PublishedClustersConfiguration.from_json(
            self.client, updated_json, self.api_path
        )

    def __repr__(self):
        return (
            f"{self.__class__.__module__}."
            f"{self.__class__.__qualname__}("
            f"dict={self._data})"
        )
