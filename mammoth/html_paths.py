import cobble
import mammoth
from . import html


def path(elements):
    return HtmlPath(elements)


def element(names, class_names=None, fresh=None, separator=None, attributes=None):
    if class_names is None:
        class_names = []
    if fresh is None:
        fresh = False
    if class_names:
        attributes= {"class": " ".join(class_names)}
    return HtmlPathElement(html.tag(
        tag_names=names,
        attributes=attributes,
        collapsible=not fresh,
        separator=separator,
    ))


@cobble.data
class HtmlPath(object):
    elements = cobble.field()
    
    def wrap(self, generate_nodes):
        nodes = generate_nodes()
        for element in reversed(self.elements):
            nodes = element.wrap_nodes(nodes)
        
        return nodes


@cobble.data
class HtmlPathElement(object):
    tag = cobble.field()

    def wrap(self, generate_nodes):
        return self.wrap_nodes(generate_nodes())

    def wrap_nodes(self, nodes):
        # try:
        #     if type(nodes[0]) == mammoth.html.nodes.TextNode:
        #         print(self.tag.attributes)
        #         print(nodes[0].attributes)
        #         print(self._cobble_fields)
        #         print(dir(self.tag.attributes))
        #         self.tag.attributes = nodes[0].attributes
        # except AttributeError: pass
        # except IndexError: pass
        element = html.Element(self.tag, nodes)
        return [element]

empty = path([])

class ignore(object):
    @staticmethod
    def wrap(generate_nodes):
        return []
