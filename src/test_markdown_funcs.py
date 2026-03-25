import unittest
from textnode import TextNode, TextType
from markdownfuncs import *

class TestMarkdownFuncs(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
        
    def test_delim_bold_double(self):
        node = TextNode("This is **bold** and **more bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("more bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_delim_unmatched(self):
        node = TextNode("This is **bold text", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)
    
    def test_delim_non_text_node(self):
        node1 = TextNode("This is text", TextType.TEXT)
        node2 = TextNode("This is bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)
        expected = [node1, node2]
        self.assertEqual(new_nodes, expected)
    
    def test_delim_italic(self):
        node = TextNode("This is *italic* text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_split_nodes_delimiter_basic(self):
            node = TextNode("This is **bold** text", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
            expected = [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT)
            ]
            self.assertEqual(new_nodes, expected)
            
    def test_split_nodes_delimiter_no_delimiter(self):
        node = TextNode("This is plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [node]
        self.assertEqual(new_nodes, expected)
            
    def test_split_nodes_delimiter_multiple_delimiters(self):
        node = TextNode("This is **bold** and **more bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("more bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)
            
    def test_split_nodes_delimiter_unmatched_delimiter(self):
        node = TextNode("This is **bold text", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)
                
    def test_split_nodes_delimiter_non_text_node(self):
        node1 = TextNode("This is text", TextType.TEXT)
        node2 = TextNode("This is bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)
        expected = [node1, node2]
        self.assertEqual(new_nodes, expected)    
            
    def test_extract_markdown_images(self):
        text = "Here is an image: ![alt text](https://example.com/image.png)"
        images = extract_markdown_images(text)
        expected = [("alt text", "https://example.com/image.png")]
        self.assertEqual(images, expected)
        
    def test_extract_markdown_links(self):
        text = "Here is a link: [link text](https://example.com)"
        links = extract_markdown_links(text)
        expected = [("link text", "https://example.com")]
        self.assertEqual(links, expected)
        
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://example.com) and another [second link](https://example.org)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://example.org"
                ),
            ],
            new_nodes,
        )
        
    def test_text_to_textnodes(self):
        text = "This is **bold** and *italic* text with a [link](https://example.com) and an ![image](https://i.imgur.com/zjjcJKZ.png)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" and an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        self.assertEqual(nodes, expected)
    
    def test_text_to_textnodes_with_code(self):
        text = "Here is some `code` in the text."
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Here is some ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" in the text.", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)
    
    def test_text_to_textnodes_mixed(self):
        text = "**Bold** text with *italic* and `code` plus a [link](https://boot.dev) and ![image](https://example.com/img.png)."
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" text with ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" plus a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)
    
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_markdown_to_blocks_empty_lines(self):
        md = """
            This is a paragraph with empty lines above and below

            This is another paragraph

            This is yet another paragraph
            """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph with empty lines above and below",
                "This is another paragraph",
                "This is yet another paragraph",
            ],
        )
        
    def test_markdown_to_blocks_no_empty_lines(self):
        md = """This is a paragraph with no empty lines
        This is still the same paragraph
        This is yet another line in the same paragraph"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph with no empty lines\nThis is still the same paragraph\nThis is yet another line in the same paragraph"
            ],
        )
        
    def test_markdown_to_blocks_only_empty_lines(self):
        md = """


        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])
        
    def test_markdown_to_blocks_mixed_empty_and_nonempty(self):
        md = """


        This is a paragraph with empty lines above

        This is another paragraph with empty lines around it

        This is yet another paragraph with empty lines below


        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph with empty lines above",
                "This is another paragraph with empty lines around it",
                "This is yet another paragraph with empty lines below",
            ],
        )
        
    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("```\ncode\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("> Quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("- List item"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("1. List item"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("This is a paragraph."), BlockType.PARAGRAPH)
        
    def test_block_to_block_type_unordered_list(self):
        self.assertEqual(block_to_block_type("* Unordered list item"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- Unordered list item"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("+ Unordered list item"), BlockType.UNORDERED_LIST)
        
    def test_block_to_block_type_ordered_list(self):
        self.assertEqual(block_to_block_type("1. Ordered list item"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("2. Ordered list item"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("10. Ordered list item"), BlockType.ORDERED_LIST)
        
    def test_block_to_block_type_code_block(self):
        self.assertEqual(block_to_block_type("```\ncode block\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```\nprint('Hello, world!')\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```\ndef foo():\n    return 'bar'\n```"), BlockType.CODE)
        
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        ) 
        
    def test_quote(self):
        md = """
> This is a quote with **bold** text and a [link](https://example.com)
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with <b>bold</b> text and a <a href=\"https://example.com\">link</a></blockquote></div>",
        )
    def test_unordered_list(self):
        md = """
- Item 1 with *italic* text
- Item 2 with a [link](https://example.com)
- Item 3 with `code`
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1 with <i>italic</i> text</li><li>Item 2 with a <a href=\"https://example.com\">link</a></li><li>Item 3 with <code>code</code></li></ul></div>",
        )
    def test_ordered_list(self):
        md = """
1. First item with **bold** text
2. Second item with a [link](https://example.com)
3. Third item with `code`
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item with <b>bold</b> text</li><li>Second item with a <a href=\"https://example.com\">link</a></li><li>Third item with <code>code</code></li></ol></div>",
        )
    def test_mixed_content(self):
        md = """# Heading with `inline code` and a [link](https://example.com) block:
> This is a quote with **bold** text and a [link](https://example.com) block:
```
This is a code block with *asterisks* and [links](https://example.com) should not be parsed
```
- List item with _italic_ text and a [link](https://example.com) block
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading with <code>inline code</code> and a <a href=\"https://example.com\">link</a> block:</h1><blockquote>This is a quote with <b>bold</b> text and a <a href=\"https://example.com\">link</a> block:</blockquote><pre><code>This is a code block with *asterisks* and [links](https://example.com) should not be parsed\n</code></pre><ul><li>List item with <i>italic</i> text and a <a href=\"https://example.com\">link</a> block</li></ul></div>",
        )
        
    def test_extract_title_with_heading(self):
        md = """# This is the title
This is the content of the markdown file.
"""
        title = extract_title(md)
        self.assertEqual(title, "This is the title")
    
    def test_extract_title_with_multiple_headings(self):
        md = """# This is the title
## This is a subtitle
This is the content of the markdown file.
"""
        title = extract_title(md)
        self.assertEqual(title, "This is the title")
    
    def test_extract_title_with_no_headings(self):
        md = """This is the content of the markdown file.
It has no headings, so the title should be 'Untitled'.
"""        
        title = extract_title(md)
        self.assertEqual(title, "Untitled")
    
    def test_extract_title_with_heading_not_at_start(self):
        md = """This is the content of the markdown file.
# This is the title
"""
        title = extract_title(md)
        self.assertEqual(title, "This is the title")
        
if __name__ == '__main__':
    unittest.main()