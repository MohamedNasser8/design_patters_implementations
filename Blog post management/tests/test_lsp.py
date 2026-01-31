# tests/test_lsp.py
"""
Demonstrates Liskov Substitution Principle:
- Derived classes can be substituted for base classes
- All validators can be used interchangeably
- All output formats can be used interchangeably
"""

import pytest
from src.schema.post_schema import Post, PostStateEnum
from src.schema.validation import Validation, ContentValidationLength, AuthorValidation, TitleValidation, Validator
from src.schema.output_schema import OutputFormat, MarkdownOutputFormat, HTMLOutputFormat, JSONOutputFormat, PlainTextOutputFormat


class TestLSP:
    """Test that derived classes can substitute base classes"""
    
    def test_all_validators_substitutable(self):
        """Any Validation subclass can be used where Validation is expected"""
        post = Post(
            id=1,
            title="Test",
            content="This is long enough content",
            author="Author",
            tags=["test"]
        )
        
        # All validators implement Validation interface
        validators: list[Validation] = [
            ContentValidationLength(min_length=10),
            AuthorValidation(),
            TitleValidation()
        ]
        
        # Can use any validator interchangeably
        for validator in validators:
            # All should work the same way
            result = validator.validate(post)
            assert isinstance(result, bool) or isinstance(result, type(None))
    
    def test_all_output_formats_substitutable(self):
        """Any OutputFormat subclass can be used where OutputFormat is expected"""
        post = Post(
            id=1,
            title="Test Title",
            content="Test Content",
            author="Author",
            tags=["test", "demo"]
        )
        
        # All formatters implement OutputFormat interface
        formatters: list[OutputFormat] = [
            MarkdownOutputFormat(),
            HTMLOutputFormat(),
            JSONOutputFormat(),
            PlainTextOutputFormat()
        ]
        
        # Can use any formatter interchangeably
        for formatter in formatters:
            result = formatter.format(post)
            assert isinstance(result, str)
            assert len(result) > 0
            # All return strings as expected by interface
    
    def test_validator_accepts_any_validation_subclass(self):
        """Validator can work with any Validation implementation"""
        # Custom validator
        class CustomValidation(Validation):
            def validate(self, post: Post) -> bool:
                return post.id >= 0
        
        # Can mix and match any validators
        validator = Validator(min_content_length=10)
        validator.validations.append(CustomValidation())
        
        post = Post(
            id=1,
            title="Test",
            content="This is long enough content",
            author="Author",
            tags=["test"]
        )
        
        # Works with custom validator too
        assert validator.validate(post) == True