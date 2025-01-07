import pytest
from backend.app.services.chat_service import ChatService
from unittest.mock import Mock, patch

@pytest.fixture
def chat_service():
    return ChatService()

def test_detect_language():
    """Test the language detection functionality"""
    service = ChatService()
    
    # Test Python detection
    python_codes = [
        """
        import os
        from datetime import datetime
        
        def hello_world():
            print("Hello, World!")
        """,
        """
        class MyClass:
            def __init__(self):
                pass
        """
    ]
    for code in python_codes:
        assert service._detect_language(code) == "python", f"Failed to detect Python in:\n{code}"

    # Test JavaScript detection
    js_codes = [
        """
        const greeting = () => {
            console.log("Hello, World!");
        }
        """,
        """
        let x = 5;
        var y = 10;
        """
    ]
    for code in js_codes:
        assert service._detect_language(code) == "javascript", f"Failed to detect JavaScript in:\n{code}"

    # Test Java detection
    java_codes = [
        """
        public class Hello {
            public static void main(String[] args) {
                System.out.println("Hello, World!");
            }
        }
        """,
        """
        public class Test {
            void testMethod() {
                System.out.println("Test");
            }
        }
        """
    ]
    for code in java_codes:
        assert service._detect_language(code) == "java", f"Failed to detect Java in:\n{code}"

    # Test unknown language
    random_texts = [
        "This is not code",
        "x = 5  # This could be many languages",
        "print('hello')  # This could be many languages"
    ]
    for text in random_texts:
        assert service._detect_language(text) == "unknown", f"Should be unknown:\n{text}"

def test_create_system_prompt():
    """Test the system prompt creation"""
    service = ChatService()
    prompt = service._create_system_prompt()
    
    assert isinstance(prompt, str)
    assert "expert programming assistant" in prompt
    assert "code examples" in prompt
    assert "markdown" in prompt

@pytest.mark.asyncio
async def test_process_message_basic():
    """Test basic message processing without code context"""
    with patch('openai.OpenAI') as mock_openai:
        # Mock the OpenAI response
        mock_completion = Mock()
        mock_completion.choices = [
            Mock(message=Mock(content="Here's how to print Hello World in Python:\n```python\nprint('Hello, World!')\n```"))
        ]
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_completion
        
        with patch.object(ChatService, '__init__', return_value=None):
            service = ChatService()
            service.client = mock_client
            
            response = await service.process_message("How do I print Hello World in Python?")
            
            assert response["status"] == "success"
            assert "Hello World" in response["response"]
            mock_client.chat.completions.create.assert_called_once()

@pytest.mark.asyncio
async def test_process_message_with_context():
    """Test message processing with code context"""
    with patch('openai.OpenAI') as mock_openai:
        mock_completion = Mock()
        mock_completion.choices = [
            Mock(message=Mock(content="Here's how to fix your Python code:\n```python\nprint('Fixed!')\n```"))
        ]
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_completion
        
        with patch.object(ChatService, '__init__', return_value=None):
            service = ChatService()
            service.client = mock_client
            
            # Test with a more definitive Python code example
            context = {
                "code": """
                import sys
                def main():
                    print('Hello World')
                """
            }
            
            response = await service.process_message(
                "What's wrong with my code?",
                context=context
            )
            
            assert response["status"] == "success"
            assert "Fixed" in response["response"]
            
            # Get the actual messages sent to the API
            calls = mock_client.chat.completions.create.call_args
            messages = calls.kwargs['messages']
            system_message = messages[0]['content']
            
            # Verify that Python was correctly detected
            assert "working with python code" in system_message.lower()

            # Test with ambiguous code
            ambiguous_context = {
                "code": "print('Hello World')"
            }
            
            response = await service.process_message(
                "What's wrong with my code?",
                context=ambiguous_context
            )
            
            # Get the messages for ambiguous code
            calls = mock_client.chat.completions.create.call_args
            messages = calls.kwargs['messages']
            system_message = messages[0]['content']
            
            # Verify that ambiguous code is marked as unknown
            assert "working with unknown code" in system_message.lower()

@pytest.mark.asyncio
async def test_process_message_error_handling():
    """Test error handling in message processing"""
    with patch('openai.OpenAI') as mock_openai:
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        
        with patch.object(ChatService, '__init__', return_value=None):
            service = ChatService()
            service.client = mock_client
            
            with pytest.raises(Exception) as exc_info:
                await service.process_message("This will cause an error")
            
            assert "API Error" in str(exc_info.value) 