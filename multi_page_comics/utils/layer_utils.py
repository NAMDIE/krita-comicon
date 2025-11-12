from krita import Krita


def find_layer_by_name(root_node, layer_name):
'''Recursively find layer by name'''
if root_node.name() == layer_name:
return root_node

for child in root_node.childNodes():
result = find_layer_by_name(child, layer_name)
if result:
return result
return None


def get_all_paint_layers(node):
'''Get all paint layers in node hierarchy'''
layers = []
if node.type() == 'paintlayer':
layers.append(node)
for child in node.childNodes():
layers.extend(get_all_paint_layers(child))
return layers


def create_layer_hierarchy(doc, structure):
'''Create layer hierarchy from structure dict'''
root = doc.rootNode()

def create_recursive(parent, structure_node):
if structure_node['type'] == 'group':
layer = doc.createGroupLayer(structure_node['name'])
else:
layer = doc.createPaintLayer(structure_node['name'])

parent.addChildNode(layer, None)

for child in structure_node.get('children', []):
create_recursive(layer, child)

return layer

for node in structure:
create_recursive(root, node)
