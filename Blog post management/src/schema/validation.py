from abc import ABC, abstractmethod

from src.schema.post_schema import Post


class Validation(ABC):
    @abstractmethod
    def validate(self, post: Post) -> bool:
        pass

class ContentValidationLength(Validation):
    def __init__(self, min_length: int = 100):
        self.min_length = min_length
    def validate(self, post: Post) -> bool:
        if len(post.content) >= self.min_length:
            return True
        raise ValueError("Content is too short")

class AuthorValidation(Validation):
    def validate(self, post: Post) -> bool:
        if post.author is not None and post.author != "":
            return True
        raise ValueError("Author is required")

class TitleValidation(Validation):
    def validate(self, post: Post) -> bool:
        if post.title is not None and post.title != "":
            return True
        raise ValueError("Title is required")

class Validator:
    def __init__(self, min_content_length: int = 100):
        self.validations: list[Validation] = [ContentValidationLength(min_content_length), AuthorValidation(), TitleValidation()]

    def validate(self, post: Post) -> bool:
        return all(validation.validate(post) for validation in self.validations)