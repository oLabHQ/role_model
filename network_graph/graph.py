import json


class Node:
    def __init__(self, id, **extra_data):
        self.id = id
        self.data = extra_data

    def serialize(self):
        data = {
            'id': str(self.id)
        }
        data.update({str(key): str(value) for key, value in self.data.items()})
        return data


class Edge:
    def __init__(self, id, source, target, classes=[], **extra_data):
        self.id = str(id)
        self.source = str(source)
        self.target = str(target)
        self.classes = classes
        self.data = extra_data

    def serialize(self):
        data = {
            'id': str(self.id),
            'source': str(self.source),
            'target': str(self.target),
        }

        if self.classes:
            data[classes] = " ".join(self.classes)

        data.update({str(key): str(value) for key, value in self.data.items()})
        return data


class Style:
    def __init__(self, selector, css):
        self.selector = selector
        self.css = css if css else {}

    def serialize(self):
        data = {
            'selector': str(self.selector),
            'css': {str(key): str(value) for key, value in self.css.items()},
        }
        return data


class Graph:
    default_edge_extra_data = {}
    default_node_extra_data = {}

    def __init__(self, container=None, layout='cose', layout_padding=20,
                 options=None):
        self.edges = {}
        self.nodes = {}
        self.styles = {}
        self.container = container
        self.layout = layout
        self.layout_padding = layout_padding
        self.options = options or {}

    def serialize(self):
        data = {
            'container': self.container,
            'layout': {
                'name': str(self.layout),
                'padding': str(self.layout_padding)
            },
            'style': [style.serialize() for _, style in self.styles.items()],
            'elements': {
                'nodes': [node.serialize() for _, node in self.nodes.items()],
                'edges': [edge.serialize() for _, edge in self.edges.items()]
            }
        }
        data.update(self.options)
        return data

    def dumps(self, *args, **kwargs):
        return json.dumps(self.serialize(), *args, **kwargs)

    def add(self, instance):
        if instance is None:
            return instance

        if isinstance(instance, Node):
            self.nodes[instance.id] = instance
        elif isinstance(instance, Edge):
            self.edges[instance.id] = instance
        elif isinstance(instance, Style):
            self.styles[instance.selector] = instance
        else:
            raise TypeError(
                "instance must be a Node, Edge or Style, got %r",
                instance.__class__)

        return instance

    def add_edge(self, id, source, target, classes=[], **extra_data):
        _extra_data = {}

        if not classes and 'classes' in self.default_edge_extra_data:
            classes = self.default_edge_extra_data.pop('classes')

        _extra_data.update(self.default_edge_extra_data)
        _extra_data.update(extra_data)

        edge = Edge(id, source, target, classes=[], **_extra_data)
        self.edges[edge.id] = edge
        return edge

    def add_node(self, id, **extra_data):
        _extra_data = {}
        _extra_data.update(self.default_edge_extra_data)
        _extra_data.update(extra_data)
        node = Node(id, **_extra_data)
        self.nodes[node.id] = node
        return node

    def add_style(self, selector, css=None, update=False):
        style = Style(selector, css.copy() if css else {})
        self.add(style)
        return style

    def update_style(self, selector, css=None):
        if selector not in self.styles:
            return self.add_style(selector, css)
        self.styles[selector].css.update(css or {})
        return self.styles[selector]
