from wagtail.contentstate import link_entity
from wagtail import hooks
from wagtail import features as draftail_features
from wagtail.html_to_contentstate import (
    HorizontalRuleHandler,
    BlockElementHandler,
    ListElementHandler,
    ListItemElementHandler,
    InlineStyleElementHandler,
    ExternalLinkElementHandler,
    PageLinkElementHandler,
)
from wagtail.rich_text import expand_db_html, features as features_registry
from wagtail.contentstate import ContentstateConverter
from draftjs_exporter.dom import DOM


def ugettext(str):
    return str


@hooks.register("register_rich_text_features")
def register_core_features(features):
    # Draftail
    features.register_editor_plugin(
        "draftail", "hr", draftail_features.BooleanFeature("enableHorizontalRule")
    )
    features.register_converter_rule(
        "contentstate",
        "hr",
        {
            "from_database_format": {"hr": HorizontalRuleHandler()},
            "to_database_format": {
                "entity_decorators": {
                    "HORIZONTAL_RULE": lambda props: DOM.create_element("hr")
                }
            },
        },
    )

    features.register_editor_plugin(
        "draftail",
        "h1",
        draftail_features.BlockFeature(
            {
                "label": "H1",
                "type": "header-one",
                "description": ugettext("Heading {level}").format(level=1),
            }
        ),
    )
    features.register_converter_rule(
        "contentstate",
        "h1",
        {
            "from_database_format": {"h1": BlockElementHandler("header-one")},
            "to_database_format": {"block_map": {"header-one": "h1"}},
        },
    )
    features.register_editor_plugin(
        "draftail",
        "h2",
        draftail_features.BlockFeature(
            {
                "label": "H2",
                "type": "header-two",
                "description": ugettext("Heading {level}").format(level=2),
            }
        ),
    )
    features.register_converter_rule(
        "contentstate",
        "h2",
        {
            "from_database_format": {"h2": BlockElementHandler("header-two")},
            "to_database_format": {"block_map": {"header-two": "h2"}},
        },
    )
    features.register_editor_plugin(
        "draftail",
        "h3",
        draftail_features.BlockFeature(
            {
                "label": "H3",
                "type": "header-three",
                "description": ugettext("Heading {level}").format(level=3),
            }
        ),
    )
    features.register_converter_rule(
        "contentstate",
        "h3",
        {
            "from_database_format": {"h3": BlockElementHandler("header-three")},
            "to_database_format": {"block_map": {"header-three": "h3"}},
        },
    )
    features.register_editor_plugin(
        "draftail",
        "h4",
        draftail_features.BlockFeature(
            {
                "label": "H4",
                "type": "header-four",
                "description": ugettext("Heading {level}").format(level=4),
            }
        ),
    )
    features.register_converter_rule(
        "contentstate",
        "h4",
        {
            "from_database_format": {"h4": BlockElementHandler("header-four")},
            "to_database_format": {"block_map": {"header-four": "h4"}},
        },
    )
    features.register_editor_plugin(
        "draftail",
        "h5",
        draftail_features.BlockFeature(
            {
                "label": "H5",
                "type": "header-five",
                "description": ugettext("Heading {level}").format(level=5),
            }
        ),
    )
    features.register_converter_rule(
        "contentstate",
        "h5",
        {
            "from_database_format": {"h5": BlockElementHandler("header-five")},
            "to_database_format": {"block_map": {"header-five": "h5"}},
        },
    )
    features.register_editor_plugin(
        "draftail",
        "h6",
        draftail_features.BlockFeature(
            {
                "label": "H6",
                "type": "header-six",
                "description": ugettext("Heading {level}").format(level=6),
            }
        ),
    )
    features.register_converter_rule(
        "contentstate",
        "h6",
        {
            "from_database_format": {"h6": BlockElementHandler("header-six")},
            "to_database_format": {"block_map": {"header-six": "h6"}},
        },
    )
    features.register_editor_plugin(
        "draftail",
        "ul",
        draftail_features.BlockFeature(
            {
                "type": "unordered-list-item",
                "icon": "list-ul",
                "description": ugettext("Bulleted list"),
            }
        ),
    )
    features.register_converter_rule(
        "contentstate",
        "ul",
        {
            "from_database_format": {
                "ul": ListElementHandler("unordered-list-item"),
                "li": ListItemElementHandler(),
            },
            "to_database_format": {
                "block_map": {"unordered-list-item": {"element": "li", "wrapper": "ul"}}
            },
        },
    )
    features.register_editor_plugin(
        "draftail",
        "ol",
        draftail_features.BlockFeature(
            {
                "type": "ordered-list-item",
                "icon": "list-ol",
                "description": ugettext("Numbered list"),
            }
        ),
    )
    features.register_converter_rule(
        "contentstate",
        "ol",
        {
            "from_database_format": {
                "ol": ListElementHandler("ordered-list-item"),
                "li": ListItemElementHandler(),
            },
            "to_database_format": {
                "block_map": {"ordered-list-item": {"element": "li", "wrapper": "ol"}}
            },
        },
    )
    features.register_editor_plugin(
        "draftail",
        "blockquote",
        draftail_features.BlockFeature(
            {
                "type": "blockquote",
                "icon": "openquote",
                "description": ugettext("Blockquote"),
            }
        ),
    )
    features.register_converter_rule(
        "contentstate",
        "blockquote",
        {
            "from_database_format": {"blockquote": BlockElementHandler("blockquote")},
            "to_database_format": {"block_map": {"blockquote": "blockquote"}},
        },
    )

    features.register_editor_plugin(
        "draftail",
        "bold",
        draftail_features.InlineStyleFeature(
            {"type": "BOLD", "icon": "bold", "description": ugettext("Bold")}
        ),
    )
    features.register_converter_rule(
        "contentstate",
        "bold",
        {
            "from_database_format": {
                "b": InlineStyleElementHandler("BOLD"),
                "strong": InlineStyleElementHandler("BOLD"),
            },
            "to_database_format": {"style_map": {"BOLD": "b"}},
        },
    )
    features.register_editor_plugin(
        "draftail",
        "italic",
        draftail_features.InlineStyleFeature(
            {"type": "ITALIC", "icon": "italic", "description": ugettext("Italic")}
        ),
    )
    features.register_converter_rule(
        "contentstate",
        "italic",
        {
            "from_database_format": {
                "i": InlineStyleElementHandler("ITALIC"),
                "em": InlineStyleElementHandler("ITALIC"),
            },
            "to_database_format": {"style_map": {"ITALIC": "i"}},
        },
    )

    features.register_editor_plugin(
        "draftail",
        "link",
        draftail_features.EntityFeature(
            {
                "type": "LINK",
                "icon": "link",
                "description": ugettext("Link"),
                # We want to enforce constraints on which links can be pasted into rich text.
                # Keep only the attributes Wagtail needs.
                "attributes": ["url", "id", "parentId"],
                "whitelist": {
                    # Keep pasted links with http/https protocol, and not-pasted links (href = undefined).
                    "href": "^(http:|https:|undefined$)"
                },
            },
            js=["wagtailadmin/js/page-chooser-modal.js"],
        ),
    )
    features.register_converter_rule(
        "contentstate",
        "link",
        {
            "from_database_format": {
                "a[href]": ExternalLinkElementHandler("LINK"),
                'a[linktype="page"]': PageLinkElementHandler("LINK"),
            },
            "to_database_format": {"entity_decorators": {"LINK": link_entity}},
        },
    )
    features.register_editor_plugin(
        "draftail",
        "superscript",
        draftail_features.InlineStyleFeature(
            {
                "type": "SUPERSCRIPT",
                "icon": "superscript",
                "description": ugettext("Superscript"),
            }
        ),
    )
    features.register_converter_rule(
        "contentstate",
        "superscript",
        {
            "from_database_format": {"sup": InlineStyleElementHandler("SUPERSCRIPT")},
            "to_database_format": {"style_map": {"SUPERSCRIPT": "sup"}},
        },
    )
    features.register_editor_plugin(
        "draftail",
        "subscript",
        draftail_features.InlineStyleFeature(
            {
                "type": "SUBSCRIPT",
                "icon": "subscript",
                "description": ugettext("Subscript"),
            }
        ),
    )
    features.register_converter_rule(
        "contentstate",
        "subscript",
        {
            "from_database_format": {"sub": InlineStyleElementHandler("SUBSCRIPT")},
            "to_database_format": {"style_map": {"SUBSCRIPT": "sub"}},
        },
    )
    features.register_editor_plugin(
        "draftail",
        "strikethrough",
        draftail_features.InlineStyleFeature(
            {
                "type": "STRIKETHROUGH",
                "icon": "strikethrough",
                "description": ugettext("Strikethrough"),
            }
        ),
    )
    features.register_converter_rule(
        "contentstate",
        "strikethrough",
        {
            "from_database_format": {"s": InlineStyleElementHandler("STRIKETHROUGH")},
            "to_database_format": {"style_map": {"STRIKETHROUGH": "s"}},
        },
    )
    features.register_editor_plugin(
        "draftail",
        "code",
        draftail_features.InlineStyleFeature(
            {"type": "CODE", "icon": "code", "description": ugettext("Code")}
        ),
    )
    features.register_converter_rule(
        "contentstate",
        "code",
        {
            "from_database_format": {"code": InlineStyleElementHandler("CODE")},
            "to_database_format": {"style_map": {"CODE": "code"}},
        },
    )


converter = ContentstateConverter(
    [
        "hr",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "ul",
        "ol",
        "blockquote",
        "bold",
        "italic",
        "link",
        "superscript",
        "subscript",
        "strikethrough",
        "code",
    ]
)

