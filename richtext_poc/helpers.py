import copy
import os

import bleach
import markdown
from bleach_whitelist import markdown_tags, markdown_attrs
from django.utils.safestring import mark_safe
from wagtail.core import hooks
from wagtail.core.models import Page


def render_markdown(text, context=None):
    allowed_table_tags = ["table", "thead", "tbody", "tfoot", "tr", "th", "td"]
    allowed_tags = markdown_tags + allowed_table_tags
    html = markdown.markdown(
        text, extensions=["tables", "smarty", LinkerExtension()], output_format="html5"
    )
    sanitised_html = bleach.clean(html, tags=allowed_tags, attributes=markdown_attrs)
    return mark_safe(sanitised_html)


class LinkPattern(markdown.inlinepatterns.LinkPattern):
    def sanitize_url(self, url):
        if url.startswith("slug:"):
            slug = url.split(":")[1]
            page = Page.objects.get(slug=slug).specific
            url = page.url
        return super().sanitize_url(url)


class LinkerExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns["link"] = LinkPattern(markdown.inlinepatterns.LINK_RE, md)
