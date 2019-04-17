import cProfile
import json
import os
import unittest
from pstats import Stats

from core.helpers import render_markdown
from wagtail.rich_text import expand_db_html

from markdown_exporter import exporter
from wagtail_features import converter


# from draftjs_exporter.constants import BLOCK_TYPES, ENTITY_TYPES
# from draftjs_exporter.defaults import BLOCK_MAP, STYLE_MAP
# from draftjs_exporter.dom import DOM
# from draftjs_exporter.html import HTML
# from tests.test_composite_decorators import BR_DECORATOR, HASHTAG_DECORATOR, LINKIFY_DECORATOR
# from tests.test_entities import hr, image, link

fixtures_path = os.path.join(os.path.dirname(__file__), "test_exports.json")
fixtures = json.loads(open(fixtures_path, "r").read())

# exporter = HTML(
#     {
#         "entity_decorators": {
#             ENTITY_TYPES.LINK: link,
#             ENTITY_TYPES.HORIZONTAL_RULE: hr,
#             ENTITY_TYPES.IMAGE: image,
#             ENTITY_TYPES.EMBED: None,
#         },
#         "composite_decorators": [BR_DECORATOR, LINKIFY_DECORATOR, HASHTAG_DECORATOR],
#         "block_map": dict(
#             BLOCK_MAP,
#             **{
#                 BLOCK_TYPES.UNORDERED_LIST_ITEM: {
#                     "element": "li",
#                     "wrapper": "ul",
#                     "wrapper_props": {"class": "bullet-list"},
#                 }
#             }
#         ),
#         "style_map": dict(
#             STYLE_MAP,
#             **{
#                 "KBD": "kbd",
#                 "HIGHLIGHT": {
#                     "element": "strong",
#                     "props": {"style": {"textDecoration": "underline"}},
#                 },
#             }
#         ),
#     }
# )


class TestExportsMeta(type):
    """
    Generates test cases dynamically.
    See http://stackoverflow.com/a/20870875/1798491
    """

    def __new__(mcs, name, bases, tests):
        def gen_test(content, html):
            def test(self):
                # self.assertEqual(exporter.render(content), html)
                # raw_content_state_string = converter.from_database_format(
                #     render_markdown(content)
                # )
                # raw_content_state = json.loads(raw_content_state_string)
                # markdown = exporter.render(raw_content_state)[:-4]
                # self.assertEqual(
                #    content.replace("\r", "").replace("\n", "").replace(' ', "")
                #    markdown.replace("\r", "").replace("\n", "").replace(' ', ""),
                # )
                raw_content_state_string = converter.from_database_format(
                    render_markdown(content)
                )
                dbhtml = converter.to_database_format(raw_content_state_string)
                # markdown = exporter.render(raw_content_state)[:-4]
                self.assertEqual(
                    html.replace("\r", "").replace("\n", "").replace(" ", ""),
                    expand_db_html(dbhtml)
                    .replace("\r", "")
                    .replace("\n", "")
                    .replace(" ", ""),
                )

            return test

        engine = name.replace("TestExports", "").lower()

        for export in fixtures:
            if ("skip" not in export) and export["markdown"] not in [None, ""]:
                # test_label = export["label"].lower().replace(" ", "_")
                test_label = export["model"] + export["field"]
                test_name = "test_export_{0}_{1}".format(engine, test_label)
                content = export["markdown"]
                html = export["html"]
                tests[test_name] = gen_test(content, html)

        return type.__new__(mcs, name, bases, tests)


class TestExportsMarkdown(unittest.TestCase, metaclass=TestExportsMeta):
    @classmethod
    def setUpClass(cls):
        cls.pr = cProfile.Profile()
        cls.pr.enable()
        print("\nmarkdown")

    @classmethod
    def tearDownClass(cls):
        cls.pr.disable()
        Stats(cls.pr).strip_dirs().sort_stats("cumulative").print_stats(0)


if __name__ == "__main__":
    unittest.main()
