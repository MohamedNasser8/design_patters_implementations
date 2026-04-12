from enum import Enum
from logger.logger import get_logger, LoggerType

console_logger = get_logger("console", LoggerType.CONSOLE)

class PostStateEnum(Enum):
    DRAFT = "unpublish"
    PUBLISH = "publish"
    ARCHIVED = "archive"


class PostState:
    def __init__(self, state: PostStateEnum, title: str):
        self.state = state
        self.title = title
    
    def archive(self) -> None:
        if self.state == PostStateEnum.ARCHIVED or self.state == PostStateEnum.DRAFT:
            raise ValueError("You can only archive a published post")
        self.state = PostStateEnum.ARCHIVED
        console_logger.log(f"Post {self.title} archived ", "info")
    
    def publish(self) -> None:
        if self.state == PostStateEnum.PUBLISH or self.state == PostStateEnum.ARCHIVED:
            raise ValueError("You can only publish a draft post")
        self.state = PostStateEnum.PUBLISH
        console_logger.log(f"Post {self.title} published", "info")
    
    def unpublish(self) -> None:
        if self.state == PostStateEnum.DRAFT or self.state == PostStateEnum.PUBLISH:
            raise ValueError("You can only unpublish an archived post")
        self.state = PostStateEnum.DRAFT
        console_logger.log(f"Post {self.title} unpublished", "info")

    def get_state(self) -> PostStateEnum:
        return self.state
    
class Post():
    def __init__(self,id: int, title: str, content: str, author: str, tags: list[str], state: PostState = PostStateEnum.DRAFT):
        self.title = title
        self.content = content
        self.author = author
        self.tags = tags
        self.state = PostState(state, title)
        self.id = id
    
    def __str__(self) -> str:
        return f"Post(id={self.id}, title={self.title}, content={self.content}, author={self.author}, tags={self.tags}, state={self.state.get_state()})"

    def update(self, **keyargs) -> None:
        for key, value in keyargs.items():
            setattr(self, key, value)