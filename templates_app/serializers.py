from rest_framework import serializers
from templates_app.models import Template


class TemplateSerializer(serializers.ModelSerializer):
    # campo apenas para upload, não é salvo no banco
    file = serializers.FileField(write_only=True, required=True)

    class Meta:
        model = Template
        fields = '__all__'
        read_only_fields = ['id', 'placeholders', 'created_at']

    def create(self, validated_data):
        uploaded_file = validated_data.pop('file')
        binary_content = uploaded_file.read()

        template = Template.objects.create(
            name=validated_data.get('name'),
            file_content=binary_content,
        )
        return template
