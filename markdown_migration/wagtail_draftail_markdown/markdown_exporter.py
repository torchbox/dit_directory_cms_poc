from draftjs_exporter.html import HTML
from draftjs_exporter_markdown import ENGINE, ENTITY_DECORATORS, STYLE_MAP

from draftjs_exporter.constants import BLOCK_TYPES, ENTITY_TYPES, INLINE_STYLES
from draftjs_exporter.defaults import STYLE_MAP as HTML_STYLE_MAP
from draftjs_exporter.defaults import BLOCK_MAP as HTML_BLOCK_MAP

from draftjs_exporter.dom import DOM


def get_block_index(blocks, key):
    """Retrieves the index at which a given block is, or -1 if not found."""
    keys = [i for i in range(len(blocks)) if blocks[i]["key"] == key]
    return keys[0] if keys else -1


def get_li_suffix(props):
    """Determines the suffix for list items (newline, or double newline) based on the next block."""
    key = props["block"].get("key")

    if not key:
        return "\r\n"

    blocks = props["blocks"]
    i = get_block_index(blocks, key)
    next_block_type = blocks[i + 1]["type"] if i + 1 < len(blocks) else None

    return "\r\n\r\n" if next_block_type != props["block"]["type"] else "\r\n"


def get_numbered_li_prefix(props):
    """Determines the prefix for numbered list items, based on its preceding blocks."""
    type_ = props["block"]["type"]
    depth = props["block"]["depth"]
    key = props["block"].get("key")

    if not key:
        return " "

    index = 1
    for block in props["blocks"]:
        # This is the current block, stop there.
        if block["key"] == key:
            break

        # The block's list hasn't started yet: reset the index.
        if block["type"] != type_:
            index = 1
        else:
            # We are in the list, but the depth is lower than that of our block: reset.
            if block["depth"] < depth:
                index = 1
            # Same list, same depth as our block: increment.
            elif block["depth"] == depth:
                index += 1

    return "%s. " % index


def list_item(prefix, props):
    """List item formatting - not really inline, not really a block either."""
    indent = "  " * props["block"]["depth"]
    suffix = get_li_suffix(props)

    return DOM.create_element(
        "fragment", {}, [indent, prefix, props["children"], suffix]
    )


def inline(children):
    """Inline formatting, eg. bold, links, code."""
    return DOM.create_element("fragment", {}, children)


def block(children):
    """Block formatting. In Markdown, blocks are followed by an empty line."""
    return DOM.create_element("fragment", {}, children + ["\r\n\r\n"])


def prefixed_block(prefix):
    return lambda props: block([prefix, props["children"]])


def ul(props):
    return list_item("* ", props)


def ol(props):
    prefix = get_numbered_li_prefix(props)
    return list_item(prefix, props)


def list_wrapper(props):
    return inline([])


BLOCK_MAP = dict(
    HTML_BLOCK_MAP,
    **{
        BLOCK_TYPES.UNSTYLED: prefixed_block(""),
        BLOCK_TYPES.HEADER_ONE: prefixed_block("# "),
        BLOCK_TYPES.HEADER_TWO: prefixed_block("## "),
        BLOCK_TYPES.HEADER_THREE: prefixed_block("### "),
        BLOCK_TYPES.HEADER_FOUR: prefixed_block("#### "),
        BLOCK_TYPES.HEADER_FIVE: prefixed_block("##### "),
        BLOCK_TYPES.HEADER_SIX: prefixed_block("###### "),
        BLOCK_TYPES.UNORDERED_LIST_ITEM: {"element": ul, "wrapper": list_wrapper},
        BLOCK_TYPES.ORDERED_LIST_ITEM: {"element": ol, "wrapper": list_wrapper},
        BLOCK_TYPES.BLOCKQUOTE: prefixed_block("> "),
        # BLOCK_TYPES.CODE: {"element": code_element, "wrapper": code_wrapper},
    }
)

exporter = HTML(
    {
        # Those configurations are overridable like for draftjs_exporter.
        "block_map": BLOCK_MAP,
        "style_map": STYLE_MAP,
        "entity_decorators": ENTITY_DECORATORS,
        "engine": ENGINE,
    }
)


def render(content):
    return exporter.render(content)[:-4]
