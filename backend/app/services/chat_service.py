from openai import OpenAI
from backend.app.core.config import settings
import re

class ChatService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
    def _detect_language(self, code: str) -> str:
        # More specific patterns for each language
        definitive_patterns = {
            'python': r'(^|\n)\s*(import\s+[a-zA-Z_]\w*|from\s+[a-zA-Z_]\w*\s+import|def\s+[a-zA-Z_]\w*\s*\(|class\s+[a-zA-Z_]\w*\s*:)',
            'javascript': r'(const|let|var|function)\s+[a-zA-Z_$]\w*|console\.',
            'java': r'(public\s+class|void\s+main|System\.out\.println)',
            'cpp': r'(#include|std::|\w+\s+\w+;$)',
        }
        
        if not code:
            return "unknown"
            
        # Check for definitive language patterns first
        for lang, pattern in definitive_patterns.items():
            if re.search(pattern, code, re.MULTILINE):
                return lang
        
        return "unknown"
    
    def _create_system_prompt(self) -> str:
        return """You are an expert programming assistant and productivity tool. 
        When providing code examples, ensure they are well-commented and follow best practices.
        For debugging, analyze the code carefully and suggest specific solutions.
        Always format code blocks properly using markdown."""
    
    async def process_message(self, message: str, context: dict = None) -> dict:
        try:
            messages = [
                {"role": "system", "content": self._create_system_prompt()},
                {"role": "user", "content": message}
            ]
            
            if context and 'code' in context:
                lang = self._detect_language(context['code'])
                messages[0]["content"] += f"\nThe user is working with {lang} code."
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7
            )
            
            return {
                "response": response.choices[0].message.content,
                "status": "success"
            }
                
        except Exception as e:
            print(f"Error in process_message: {str(e)}")  # Add logging
            raise Exception(f"Error processing message: {str(e)}") 