from typing import Optional, Dict, Any, List
from krita import Krita


def find_layer_by_name(root_node, layer_name: str):
    """Recursively find layer by name.
    
    Args:
        root_node: Root layer to search from
        layer_name: Name of layer to find
        
    Returns:
        Layer node if found, None otherwise
    """
    if root_node.name() == layer_name:
        return root_node

    for child in root_node.childNodes():
        result = find_layer_by_name(child, layer_name)
        if result:
            return result
    return None


def get_all_paint_layers(node) -> List:
    """Get all paint layers in node hierarchy.
    
    Args:
        node: Root node to search
        
    Returns:
        List of paint layer nodes
    """
    layers = []
    if node.type() == 'paintlayer':
        layers.append(node)
    for child in node.childNodes():
        layers.extend(get_all_paint_layers(child))
    return layers


def create_layer_hierarchy(doc, structure: List[Dict[str, Any]]) -> None:
    """Create layer hierarchy from structure dict.
    
    Args:
        doc: Krita document
        structure: List of layer structure dictionaries
    """
    root = doc.rootNode()

    def create_recursive(parent, structure_node: Dict[str, Any]):
        """Recursively create layer structure.
        
        Args:
            parent: Parent layer
            structure_node: Node definition
        """
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