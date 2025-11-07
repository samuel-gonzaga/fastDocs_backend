from rest_framework.renderers import JSONRenderer

class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        # Se o retorno for bytes (ex: arquivo .docx), não tenta renderizar como JSON
        if isinstance(data, (bytes, bytearray)):
            return data

        response = renderer_context.get('response', None)

        success = True
        if response is not None and response.status_code >= 400:
            success = False

        # Garante que data é um dict antes de manipular
        if not isinstance(data, dict):
            data = {'data': data}

        response_data = {
            'success': success,
            'data': data if data is not None else {}
        }

        if 'detail' in data:
            response_data['message'] = data['detail']
            response_data['data'].pop('detail', None)

        if 'success' in data:
            data.pop('success', None)

        return super().render(response_data, accepted_media_type, renderer_context)
