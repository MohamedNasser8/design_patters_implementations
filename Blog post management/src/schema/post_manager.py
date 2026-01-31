from schema.post_schema import Post
from logger.logger import get_logger, LoggerType
from schema.validation import Validator

console_logger = get_logger("console", LoggerType.CONSOLE)

class PostManager:
    def __init__(self, validator: Validator):
        self.posts: list[Post] = []
        self.validator = validator
    
    def add_post(self, title: str, content: str, author: str, tags: list[str]) -> Post:
        new_post = Post(id=len(self.posts), title=title, content=content, author=author, tags=tags)
        if not self.validator.validate(new_post):
            raise ValueError("Post is invalid")
        self.posts.append(new_post)
        console_logger.log(f"Post {new_post.title} added", "info")
        return new_post
    
    def get_posts(self) -> list[Post]:
        return self.posts
    
    def get_post(self, id: int) -> Post:
        return self.posts[id]
    
    def update_post(self, **keyargs) -> Post:
        post = self.get_post(keyargs["id"])
        post.update(**keyargs)
        if not self.validator.validate(post):
            raise ValueError("Post is invalid")
        self.posts[post.id] = post
        console_logger.log(f"Post {post.title} updated", "info")
        return post

    def archive_post(self, id: int) -> Post:
        post = self.get_post(id)
        post.state.archive()
        self.posts[post.id] = post
        console_logger.log(f"Post {post.title} archived", "info")
        return post
    
    def publish_post(self, id: int) -> Post:
        post = self.get_post(id)
        post.state.publish()
        self.posts[post.id] = post
        console_logger.log(f"Post {post.title} published", "info")
        return post
    
    def unpublish_post(self, id: int) -> Post:
        post = self.get_post(id)
        post.state.unpublish()
        self.posts[post.id] = post
        console_logger.log(f"Post {post.title} unpublished", "info")
        return post