import json

from django.views.generic import TemplateView


class GraphView(TemplateView):
    template_name = "network_graph/network_graph.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'graph_data': json.dumps(self.graph().serialize())
        })

    def graph(self):
        raise NotImplementedError
