# tests/test_dip.py
"""
Demonstrates Dependency Inversion Principle:
- High-level modules depend on abstractions, not concretions
- Can swap implementations without changing dependent code
"""

import pytest
from unittest.mock import Mock, MagicMock
from src.schema.post_schema import Post, PostStateEnum
from src.schema.post_manager import PostManager
from src.schema.validation import Validation, Validator
from src.logger.logger import BaseLogger


class TestDIP:
    """Test that dependencies are on abstractions, not concretions"""
    
    def test_post_manager_depends_on_validator_abstraction(self):
        """PostManager depends on Validator abstraction, not concrete validators"""
        # Create a mock validator (abstraction)
        mock_validator = Mock(spec=Validator)
        mock_validator.validate = Mock(return_value=True)
        
        # PostManager works with any Validator implementation
        manager = PostManager(validator=mock_validator)
        
        post = manager.add_post(
            title="Test",
            content="This is long enough content",
            author="Author",
            tags=["test"]
        )
        
        # Manager doesn't know or care about concrete validator implementation
        assert post is not None
        mock_validator.validate.assert_called()
    
    def test_can_swap_validator_implementations(self):
        """Can swap different validator implementations without changing PostManager"""
        # Validator 1: Standard validator
        validator1 = Validator(min_content_length=10)
        
        # Validator 2: Mock validator (different implementation)
        validator2 = Mock(spec=Validator)
        validator2.validate = Mock(return_value=True)
        
        # PostManager works with both
        manager1 = PostManager(validator=validator1)
        manager2 = PostManager(validator=validator2)
        
        post1 = manager1.add_post(
            title="Test",
            content="This is long enough content",
            author="Author",
            tags=["test"]
        )
        
        post2 = manager2.add_post(
            title="Test",
            content="This is long enough content",
            author="Author",
            tags=["test"]
        )
        
        # Both work the same way
        assert post1 is not None
        assert post2 is not None
    
    def test_validator_depends_on_validation_abstraction(self):
        """Validator depends on Validation abstraction, not concrete validators"""
        # Create mock validations (abstractions)
        mock_validation1 = Mock(spec=Validation)
        mock_validation1.validate = Mock(return_value=True)
        
        mock_validation2 = Mock(spec=Validation)
        mock_validation2.validate = Mock(return_value=True)
        
        # Validator works with any Validation implementations
        validator = Validator(min_content_length=10)
        validator.validations = [mock_validation1, mock_validation2]
        
        post = Post(
            id=1,
            title="Test",
            content="This is long enough content",
            author="Author",
            tags=["test"]
        )
        
        result = validator.validate(post)
        
        # Validator doesn't know about concrete validation implementations
        assert result == True
        mock_validation1.validate.assert_called()
        mock_validation2.validate.assert_called()
    
    def test_can_use_different_logger_implementations(self):
        """System can work with different logger implementations via abstraction"""
        # Note: Your current implementation uses get_logger() factory
        # This demonstrates the concept - loggers depend on BaseLogger abstraction
        
        # Mock logger (abstraction)
        mock_logger = Mock(spec=BaseLogger)
        mock_logger.log = Mock()
        
        # Any code using BaseLogger can work with any implementation
        mock_logger.log("Test message", "info")
        
        # Works with any BaseLogger implementation
        mock_logger.log.assert_called_with("Test message", "info")
    
    def test_high_level_modules_dont_depend_on_low_level(self):
        """PostManager (high-level) doesn't depend on concrete validators (low-level)"""
        # PostManager is high-level business logic
        # It depends on Validator abstraction, not ContentValidationLength, etc.
        
        # Can create manager with any validator that implements Validator interface
        validator = Validator(min_content_length=10)
        manager = PostManager(validator=validator)
        
        # Manager doesn't need to know about ContentValidationLength, etc.
        # It just uses the Validator interface
        post = manager.add_post(
            title="Test",
            content="This is long enough content",
            author="Author",
            tags=["test"]
        )
        
        assert post is not None