from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn
from backend.app.services.chat_service import ChatService

app = FastAPI(
    title="Code Assistant & Productivity Bot",
    description="""
    An intelligent programming assistant that helps with code analysis, 
    debugging, and productivity tracking.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    """
    Chat message model with optional code context
    """
    message: str
    context: Optional[dict] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "How do I write a hello world program in Python?",
                "context": {
                    "code": "print('Hello')"
                }
            }
        }
    }

# Initialize chat service
chat_service = ChatService()

@app.get("/", response_class=HTMLResponse)
async def root():
    """
    Simple HTML interface for the chat bot
    """
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Code Assistant Chat</title>
            <style>
                body { max-width: 800px; margin: 0 auto; padding: 20px; font-family: Arial, sans-serif; }
                #chat-container { height: 400px; overflow-y: auto; border: 1px solid #ccc; padding: 10px; margin-bottom: 20px; }
                #input-container { display: flex; gap: 10px; }
                #message-input { flex-grow: 1; padding: 10px; }
                button { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
                .message { margin: 10px 0; padding: 10px; border-radius: 5px; }
                .user-message { background: #e9ecef; }
                .bot-message { background: #f8f9fa; }
                pre { background: #f8f9fa; padding: 10px; border-radius: 5px; overflow-x: auto; }
            </style>
        </head>
        <body>
            <h1>Code Assistant Chat</h1>
            <div id="chat-container"></div>
            <div id="input-container">
                <textarea id="message-input" placeholder="Type your message here..." rows="3"></textarea>
                <button onclick="sendMessage()">Send</button>
            </div>
            <script>
                async function sendMessage() {
                    const input = document.getElementById('message-input');
                    const message = input.value.trim();
                    if (!message) return;

                    // Add user message to chat
                    addMessage('user', message);
                    input.value = '';

                    try {
                        const response = await fetch('/api/chat', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({
                                message: message
                            })
                        });
                        const data = await response.json();
                        addMessage('bot', data.response);
                    } catch (error) {
                        addMessage('bot', 'Sorry, there was an error processing your request.');
                    }
                }

                function addMessage(type, content) {
                    const container = document.getElementById('chat-container');
                    const messageDiv = document.createElement('div');
                    messageDiv.className = `message ${type}-message`;
                    
                    // Check if content contains code blocks and format them
                    if (content.includes('```')) {
                        const parts = content.split('```');
                        let formattedContent = parts[0];
                        for (let i = 1; i < parts.length; i += 2) {
                            const code = parts[i].trim();
                            formattedContent += `<pre><code>${code}</code></pre>`;
                            if (parts[i + 1]) formattedContent += parts[i + 1];
                        }
                        messageDiv.innerHTML = formattedContent;
                    } else {
                        messageDiv.textContent = content;
                    }
                    
                    container.appendChild(messageDiv);
                    container.scrollTop = container.scrollHeight;
                }

                // Handle Enter key
                document.getElementById('message-input').addEventListener('keypress', function(e) {
                    if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        sendMessage();
                    }
                });
            </script>
        </body>
    </html>
    """

@app.post("/api/chat")
async def chat(chat_message: ChatMessage):
    """
    Process a chat message and return a response
    
    - **message**: The user's message
    - **context**: Optional code context
    """
    try:
        response = await chat_service.process_message(
            chat_message.message,
            chat_message.context
        )
        return {
            "response": response["response"],
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 