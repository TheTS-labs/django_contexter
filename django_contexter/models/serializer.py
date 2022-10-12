"""Same as ModelSerializer, but with dynamic model and fields feature."""

from rest_framework import serializers
from rest_framework.fields import empty


class Serializer(serializers.ModelSerializer):
    """Same as ModelSerializer, but with dynamic model and fields feature."""

    def __init__(self, instance=None, **kwargs):
        """
        Init with creating Meta.

        Args:
            instance : # Name from ModelSerializer
                QuerySet with records from model
            kwargs :
                model: Model instance
                fields: Fields to serialize
        """
        super().__init__(instance=instance, data=empty, **kwargs)
        self.Meta = type(
            "Meta", (Serializer,),
            {"model": self.context.get("model"), "fields": self.context.get("fields")},
        )
