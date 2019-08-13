from abc import abstractmethod


class BaseBuilder:
    def __init__(self, contained, **kwargs):
        self._contained = contained
        self.__dict__.update(**kwargs)

    def __getattr__(self, name):
        return getattr(self._contained, name)

    @abstractmethod
    def _build(self):
        pass

    @abstractmethod
    def put(self, resource_class):
        new_data = (
            self.client.put(self.api_path, json=self._build()).successful().json()
        )
        return resource_class(self.client, new_data, self.api_path)
