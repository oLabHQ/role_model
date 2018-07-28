from django.test import TestCase

from network_graph.graph import Graph, Style


class GraphTestCase(TestCase):
    def test_graph(self):
        class MonacoGraph(Graph):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.add(Style(
                    'node',
                    {
                        'font-family': 'monaco'
                    }
                ))

        self.graph = MonacoGraph()
        self.graph.add_node("1", name="hello")
        self.graph.add_node("2", name="world")
        self.graph.add_edge("3", "1", "2")
        self.graph.update_style("node", {
          'font-size': 24,
        })
        self.assertEqual(self.graph.serialize(), {
            'container': None,
            'layout': {'name': 'cose', 'padding': '20'},
            'style': [{
                'selector': 'node',
                'css': {
                    'font-family': 'monaco',
                    'font-size': '24'
                }
            }],
            'elements': {
                'nodes': [{
                    'id': '1',
                    'name': 'hello'
                },
                {
                    'id': '2',
                    'name': 'world'
                }],
                'edges': [{
                    'id': '3',
                    'source': '1',
                    'target': '2'}
                ]}
            })
