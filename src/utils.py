import re


from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode


def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(
                tag="a", value=text_node.text, props={"href": text_node.url or ""}
            )
        case TextType.IMAGE:
            return LeafNode(
                tag="img",
                value="",
                props={"src": text_node.url or "", "alt": text_node.text},
            )


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        parts = old_node.text.split(delimiter)
        if len(parts) % 2 != 1:
            raise ValueError(f"{old_node.text} is malformed markdown string")

        parsed_nodes = []
        for i in range(len(parts)):
            if not parts[i]:
                continue

            if i % 2 == 0:
                parsed_nodes.append(TextNode(parts[i], TextType.TEXT))
            else:
                parsed_nodes.append(TextNode(parts[i], text_type))

        new_nodes.extend(parsed_nodes)

    return new_nodes


def extract_markdown_images(text: str) -> list[tuple]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> list[tuple]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        images = extract_markdown_images(old_node.text)
        if not images:
            new_nodes.append(old_node)
            continue

        parsed_nodes = []
        text = old_node.text
        for image_parts in images:
            img_text, img_link = image_parts
            split_text, text = text.split(sep=f"![{img_text}]({img_link})", maxsplit=1)
            if split_text:
                parsed_nodes.append(TextNode(split_text, TextType.TEXT))
            parsed_nodes.append(TextNode(img_text, TextType.IMAGE, img_link))
        if text:
            parsed_nodes.append(TextNode(text, TextType.TEXT))
        
        new_nodes.extend(parsed_nodes)

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        links = extract_markdown_links(old_node.text)
        if not links:
            new_nodes.append(old_node)
            continue

        parsed_nodes = []
        text = old_node.text
        for link_parts in links:
            link_text, link_url = link_parts
            split_text, text = text.split(sep=f"[{link_text}]({link_url})", maxsplit=1)
            if split_text:
                parsed_nodes.append(TextNode(split_text, TextType.TEXT))
            parsed_nodes.append(TextNode(link_text, TextType.LINK, link_url))
        if text:
            parsed_nodes.append(TextNode(text, TextType.TEXT))
        
        new_nodes.extend(parsed_nodes)

    return new_nodes
