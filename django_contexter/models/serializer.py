from rest_framework import serializers
from rest_framework.fields import empty


class Serializer(serializers.ModelSerializer):
    """Same as ModelSerializer, but with dynamic model and fields feature"""

    class Meta(object):
        pass

    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance, data, **kwargs)
        setattr(Serializer.Meta, "model", self.context.get("model"))
        setattr(Serializer.Meta, "fields", self.context.get("fields"))
