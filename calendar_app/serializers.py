from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'date', 'time', 'category',
            'description', 'password',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        # valida a senha apenas para eventos "outro"
        category = data.get('category', getattr(self.instance, 'category', None))
        password = data.get('password')

        if category == 'other' and not password:
            raise serializers.ValidationError("Eventos da categoria 'Outro' precisam de senha.")
        return data

    # def create(self, validated_data):
    #     validated_data['created_by'] = self.context['request'].user
    #     return super().create(validated_data)
