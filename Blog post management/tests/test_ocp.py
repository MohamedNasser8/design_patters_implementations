import pytest
from src.schema.post_schema import PostStateEnum, PostState, Post
from src.schema.output_schema import MarkdownOutputFormat, HTMLOutputFormat, JSONOutputFormat, PlainTextOutputFormat, OutputFormat
from src.schema.validation import Validator, Validation
from src.schema.post_manager import PostManager

class TestOCP:
    """Test that system is open for extention closed for modification"""
    
    def test_add_new_validation_rule(self):
        """Test that new validation rules can be added without modifying the existing code"""
        class TagValidation(Validation):
            def validate(self, post: Post) -> bool:
                if len(post.tags) > 0:
                    return True
                raise ValueError("Tags are required")
        
        validator = Validator(min_content_length = 10)
        validator.validations.append(TagValidation())

        post_with_tags = Post(id=1, title="Test Post", content="This is a test post", author="Test Author", tags=["test", "post"])
        post_without_tags = Post(id=2, title="Test Post", content="This is a test post", author="Test Author", tags=[])

        assert validator.validate(post_with_tags)
        with pytest.raises(ValueError):
            validator.validate(post_without_tags)

    def test_add_new_output_format(self):
        """Test that new output formats can be added without modifying the existing code"""
        class XMLOutputFormat(OutputFormat):
            def format(self, post: Post) -> str:
                return f"<post><title>{post.title}</title><content>{post.content}</content><author>{post.author}</author><tags>{', '.join(post.tags)}</tags></post>"
        
        output_format = XMLOutputFormat()
        post = Post(id=1, title="Test Post", content="This is a test post", author="Test Author", tags=["test", "post"])
        assert output_format.format(post) == "<post><title>Test Post</title><content>This is a test post</content><author>Test Author</author><tags>test, post</tags></post>"
