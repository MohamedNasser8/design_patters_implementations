from abc import ABC, abstractmethod
import json
from src.schema.post_schema import Post


class OutputFormat(ABC):
    @abstractmethod
    def format(self, post: Post) -> str:
        pass


class MarkdownOutputFormat(OutputFormat):
    def format(self, post: Post) -> str:
        return f"# {post.title}\n\n{post.content}\n\nTags: {', '.join(post.tags)}"

class HTMLOutputFormat(OutputFormat):
    def format(self, post: Post) -> str:
        return f"<h1>{post.title}</h1>\n<p>{post.content}</p>\n<p>Tags: {', '.join(post.tags)}</p>"

class JSONOutputFormat(OutputFormat):
    def format(self, post: Post) -> str:
        return json.dumps({
            "title": post.title,
            "content": post.content,
            "tags": post.tags,
        })

class PlainTextOutputFormat(OutputFormat):
    def format(self, post: Post) -> str:
        return f"{post.title}\n\n{post.content}\n\nTags: {', '.join(post.tags)}"