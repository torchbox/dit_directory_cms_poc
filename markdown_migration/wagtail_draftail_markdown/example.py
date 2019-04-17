import os
import json
from wagtail.rich_text import expand_db_html, features
from core.helpers import render_markdown

from markdown_exporter import render
from wagtail_features import converter

examples_path = os.path.join(os.path.dirname(__file__), "example.json")
examples = json.loads(open(examples_path, "r").read())

new_examples = []

for example in examples:
    if "skip" not in example and example["markdown"] is not None:
        dbhtml = render_markdown(example["markdown"])
        contentstate = converter.from_database_format(dbhtml)

        new_example = {
            "markdown": example["markdown"],
            "md_exprt": render(json.loads(contentstate)),
            "html": example["html"],
            "dbml": dbhtml,
            "exml": expand_db_html(dbhtml),
            "contentstate": contentstate,
            "model": example["model"],
            "field": example["field"],
        }
    else:
        new_example = {
            "markdown": example["markdown"],
            "md_exprt": "",
            "html": example["html"],
            "dbml": "",
            "exml": "",
            "contentstate": "",
            "model": example["model"],
            "field": example["field"],
        }

    if "skip" in example:
        new_example["skip"] = example["skip"]

    new_examples.append(new_example)

with open("example.json", "w") as j:
    j.write(json.dumps(new_examples, indent=2))


print(
    render(
        json.loads(
            converter.from_database_format(
                render_markdown("This is a [test](slug:example)")
            )
        )
    )
)

print(converter.from_database_format(render_markdown("This is a [test](slug:example)")))

print(
    converter.to_database_format(
        json.dumps(
            {
                "blocks": [
                    {
                        "key": "1wyii",
                        "type": "unstyled",
                        "depth": 0,
                        "text": "This is a test",
                        "inlineStyleRanges": [],
                        "entityRanges": [{"key": 0, "offset": 10, "length": 4}],
                    }
                ],
                "entityMap": {
                    "0": {
                        "mutability": "MUTABLE",
                        "type": "LINK",
                        "data": {"url": "http://www.example.com"},
                    }
                },
            }
        )
    )
)

