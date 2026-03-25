from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType
from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextType.LINK:
        if text_node.url is None:
            raise ValueError("invalid link: url is required")
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        if text_node.url is None:
            raise ValueError("invalid image: url is required")
        return LeafNode(tag="img", props={"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"invalid text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) == 1:
            new_nodes.append(node)
            continue
        if len(parts) % 2 == 0:
            raise ValueError(f"invalid syntax: unmatched delimiter {delimiter}")
        for i, part in enumerate(parts):
            if i % 2 == 0:
                if part:
                    new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r'!\[([^\]]+)\]\(([^)]+)\)', text)

def extract_markdown_links(text):
    return re.findall(r'\[([^\]]+)\]\(([^)]+)\)', text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        parts = re.split(r'!\[[^\]]+\]\([^)]+\)', node.text)
        for i, part in enumerate(parts):
            if part:
                new_nodes.append(TextNode(part, TextType.TEXT))
            if i < len(parts) - 1:
                alt_text, url = images[i]
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url=url))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        parts = re.split(r'\[[^\]]+\]\([^)]+\)', node.text)
        for i, part in enumerate(parts):
            if part:
                new_nodes.append(TextNode(part, TextType.TEXT))
            if i < len(parts) - 1:
                link_text, url = links[i]
                new_nodes.append(TextNode(link_text, TextType.LINK, url=url))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    # Split on double newlines first
    raw_blocks = markdown.split("\n\n")
    
    blocks = []
    for raw_block in raw_blocks:
        stripped = raw_block.strip()
        if not stripped:
            continue
            
        lines = stripped.split("\n")
        
        # Check if this block contains multiple block types mixed together
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Skip empty lines
            if not line:
                i += 1
                continue
            
            # Code blocks
            if line.startswith("```"):
                code_lines = [line]
                i += 1
                while i < len(lines):
                    code_lines.append(lines[i].strip())
                    if lines[i].strip().startswith("```"):
                        break
                    i += 1
                blocks.append("\n".join(code_lines))
                i += 1
            # Headings
            elif re.match(r'^#{1,6}\s', line):
                blocks.append(line)
                i += 1
            # Quote blocks
            elif line.startswith(">"):
                quote_lines = [line]
                i += 1
                while i < len(lines) and lines[i].strip().startswith(">"):
                    quote_lines.append(lines[i].strip())
                    i += 1
                blocks.append("\n".join(quote_lines))
            # List items
            elif re.match(r'^[-*+]\s', line) or re.match(r'^\d+\.\s', line):
                list_lines = [line]
                list_type = "unordered" if re.match(r'^[-*+]\s', line) else "ordered"
                i += 1
                while i < len(lines):
                    next_line = lines[i].strip()
                    if not next_line:
                        break
                    if list_type == "unordered" and re.match(r'^[-*+]\s', next_line):
                        list_lines.append(next_line)
                        i += 1
                    elif list_type == "ordered" and re.match(r'^\d+\.\s', next_line):
                        list_lines.append(next_line)
                        i += 1
                    else:
                        break
                blocks.append("\n".join(list_lines))
            # Paragraphs
            else:
                para_lines = [line]
                i += 1
                while i < len(lines):
                    next_line = lines[i].strip()
                    if not next_line:
                        break
                    # Stop if next line is a block marker
                    if (next_line.startswith("```") or 
                        re.match(r'^#{1,6}\s', next_line) or 
                        next_line.startswith(">") or
                        re.match(r'^[-*+]\s', next_line) or
                        re.match(r'^\d+\.\s', next_line)):
                        break
                    para_lines.append(next_line)
                    i += 1
                blocks.append("\n".join(para_lines))
    
    return blocks

def block_to_block_type(markdown_block):
    if re.match(r'^#{1,6}\s', markdown_block):
        return BlockType.HEADING
    elif markdown_block.startswith("```") and markdown_block.endswith("```"):
        return BlockType.CODE
    elif all(line.startswith(">") for line in markdown_block.split("\n")):
        return BlockType.QUOTE
    elif all(re.match(r'^\d+\.\s', line.strip()) for line in markdown_block.split("\n") if line.strip()):
        return BlockType.ORDERED_LIST
    elif all(re.match(r'^[-*+]\s', line.strip()) for line in markdown_block.split("\n") if line.strip()):
        return BlockType.UNORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            heading_match = re.match(r'^(#+)\s', block)
            heading_level = len(heading_match.group(1)) # type: ignore
            content = block.lstrip("#").strip()
            children = text_to_textnodes(content)
            html_children = [text_node_to_html_node(child) for child in children]
            block_nodes.append(ParentNode(f"h{heading_level}", html_children))
        elif block_type == BlockType.CODE:
            lines = block.split("\n")
            # Remove the triple backticks from start and end
            content_lines = lines[1:-1]
            content = "\n".join(content_lines) + "\n"
            code_node = LeafNode(tag="code", value=content)
            block_nodes.append(ParentNode("pre", [code_node]))
        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            quote_lines = [line.lstrip("> ") for line in lines]
            content = " ".join(quote_lines)
            children = text_to_textnodes(content)
            html_children = [text_node_to_html_node(child) for child in children]
            block_nodes.append(ParentNode("blockquote", html_children))
        elif block_type == BlockType.ORDERED_LIST:
            items = re.split(r'^\d+\.\s', block, flags=re.MULTILINE)[1:]
            item_nodes = []
            for item in items:
                children = text_to_textnodes(item.strip())
                html_children = [text_node_to_html_node(child) for child in children]
                item_nodes.append(ParentNode("li", html_children))
            block_nodes.append(ParentNode("ol", item_nodes))
        elif block_type == BlockType.UNORDERED_LIST:
            items = re.split(r'^[-*+]\s', block, flags=re.MULTILINE)[1:]
            item_nodes = []
            for item in items:
                children = text_to_textnodes(item.strip())
                html_children = [text_node_to_html_node(child) for child in children]
                item_nodes.append(ParentNode("li", html_children))
            block_nodes.append(ParentNode("ul", item_nodes))
        else:
            paragraph_text = block.replace("\n", " ")
            children = text_to_textnodes(paragraph_text)
            html_children = [text_node_to_html_node(child) for child in children]
            block_nodes.append(ParentNode("p", html_children))
    return ParentNode("div", block_nodes)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if re.match(r'^#{1,6}\s', line):
            return line.lstrip("#").strip()
    return "Untitled"