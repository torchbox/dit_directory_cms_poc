import bleach
import markdown
from bleach_whitelist import markdown_tags, markdown_attrs


def render_markdown(text, context=None):
    allowed_table_tags = ["table", "thead", "tbody", "tfoot", "tr", "th", "td"]
    allowed_tags = markdown_tags + allowed_table_tags
    html = markdown.markdown(
        text, extensions=["tables", "smarty", LinkerExtension()], output_format="html5"
    )
    # sanitised_html = bleach.clean(html, tags=allowed_tags, attributes=markdown_attrs)
    # return mark_safe(sanitised_html)
    return html


class LinkPattern(markdown.inlinepatterns.LinkPattern):
    def handleMatch(self, m):
        el = super(LinkPattern, self).handleMatch(m)
        href = el.get("href", "")
        if href.startswith("slug:"):
            el.set("linktype", "page")
            el.set("id", "99")
            el.attrib.pop("href")
        return el

    # def sanitize_url(self, url):
    #     if url.startswith("slug:"):
    #         slug = url.split(":")[1]
    #         # page = Page.objects.get(slug=slug).specific
    #         url = "http://www.example.com/" + slug
    #     return super().sanitize_url(url)


class LinkerExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns["link"] = LinkPattern(markdown.inlinepatterns.LINK_RE, md)

