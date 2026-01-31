from logger.logger import get_logger, LoggerType
from schema.post_manager import PostManager
from schema.validation import Validator
from schema.output_schema import MarkdownOutputFormat, HTMLOutputFormat, JSONOutputFormat, PlainTextOutputFormat


console_logger = get_logger("console", LoggerType.CONSOLE)
file_logger = get_logger("file", LoggerType.FILE)

console_logger.log("This is a test message", "info")
file_logger.log("This is a test message", "info")

validator = Validator(min_content_length = 10)
post_manager = PostManager(validator=validator)

post1 = post_manager.add_post(title="Test Post", content="This is a test post", author="Test Author", tags=["test", "post"])
print(post1)

post2 = post_manager.update_post(id=post1.id,
content="""
It is a field of study that aims to create machines that can learn and reason like humans.
It includes the development of algorithms and architectures that enable machines to learn from data, reason about the world, and make decisions.
It incorporates elements of computer science, statistics, and mathematics.
""",
author="John Doe", 
tags=["ai", "machine learning", "artificial intelligence"])
print(post2)

post_manager.publish_post(id=post2.id)
print(post_manager.get_post(post2.id))

post_manager.archive_post(id=post2.id)
print(post_manager.get_post(post2.id))

post_manager.unpublish_post(id=post2.id)
print(post_manager.get_post(post2.id))

print(MarkdownOutputFormat().format(post_manager.get_post(post2.id)))
print(HTMLOutputFormat().format(post_manager.get_post(post2.id)))
print(JSONOutputFormat().format(post_manager.get_post(post2.id)))
print(PlainTextOutputFormat().format(post_manager.get_post(post2.id)))