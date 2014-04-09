from coffin.views.generic.base import TemplateView


class MainView(TemplateView):
    template_name = 'test.html'

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        return context