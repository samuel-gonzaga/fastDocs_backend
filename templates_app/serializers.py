from rest_framework import serializers
from templates_app.models import Template


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = '__all__'
        read_only_fields = ['id', 'placeholders', 'created_at', 'updated_at']

    def create(self, validated_data):
        """
        Cria um novo template no banco de dados.
        """
        return Template.objects.create(**validated_data)
