from rest_framework import serializers

def clean_empty(data):
    if isinstance(data, dict):
        return {
            k: clean_empty(v)
            for k, v in data.items()
            if v not in (None, "", [], {})
        }
    elif isinstance(data, list):
        return [clean_empty(item) for item in data if item not in (None, "", [], {})]
    return data

class BaseCleanSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return clean_empty(rep)