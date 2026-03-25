import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(tag="a", value="Click me", props={"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')
        
    def test_values(self):
        node = HTMLNode(tag="p", value="This is a paragraph.")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "This is a paragraph.")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
        
    def test_repr(self):
        node = HTMLNode(tag="div", value="Hello", children=[], props={"class": "container"})
        expected_repr = "HTMLNode(tag=div, value=Hello, children=[], props={'class': 'container'})"
        self.assertEqual(repr(node), expected_repr)
        
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "This is a paragraph.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph.</p>")
        
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(value="Just some text.")
        self.assertEqual(node.to_html(), "Just some text.")
        
    def test_leaf_to_html_no_value(self):
        node = LeafNode(tag="p")
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),"<div><span><b>grandchild</b></span></div>",)
        
    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child", props={"class": "child-class"})
        parent_node = ParentNode("div", [child_node], props={"id": "parent-id"})
        self.assertEqual(parent_node.to_html(), '<div id="parent-id"><span class="child-class">child</span></div>')
        
    def test_parent_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()
    
    def test_parent_to_html_no_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()
    
if __name__ == '__main__':
    unittest.main()