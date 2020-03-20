from rest_framework.renderers import JSONRenderer


class EmberJSONRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        code = renderer_context["response"].status_code
        message = renderer_context["response"].status_text
        data = {'code': code, 'message': message, 'data': data}
        return super(EmberJSONRenderer, self).render(data, accepted_media_type, renderer_context)
