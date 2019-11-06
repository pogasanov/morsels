from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Optional


@dataclass
class Tag:
    name: str
    attributes: dict


class TagHTMLParser(HTMLParser):
    processed_tag: Optional[Tag]

    def handle_starttag(self, tag, attrs):
        parsed_attrs = {}
        for attr in attrs:
            try:
                k, v = attr
            except ValueError:
                parsed_attrs[attr] = None
            else:
                if k not in parsed_attrs:
                    parsed_attrs[k] = v
        self.processed_tag = Tag(name=tag, attributes=parsed_attrs)

    def parse_tag(self, data):
        self.processed_tag = None
        self.feed(data)
        return self.processed_tag


def tags_equal(tag1, tag2):
    parser = TagHTMLParser()
    tag1_data = parser.parse_tag(tag1)
    tag2_data = parser.parse_tag(tag2)
    return tag1_data == tag2_data
