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
    Enhanced HTML interface for the chat bot with better markdown formatting
    """
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Code Assistant Chat</title>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/default.min.css">
            <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
            <style>
                body { 
                    max-width: 800px; 
                    margin: 0 auto; 
                    padding: 20px; 
                    font-family: Arial, sans-serif;
                    background-color: #f5f5f5;
                }
                #chat-container { 
                    height: 500px; 
                    overflow-y: auto; 
                    border: 1px solid #ddd; 
                    padding: 20px; 
                    margin-bottom: 20px;
                    background-color: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                #input-container { 
                    display: flex; 
                    gap: 10px;
                    background-color: white;
                    padding: 15px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                #message-input { 
                    flex-grow: 1; 
                    padding: 12px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    font-size: 14px;
                    resize: vertical;
                }
                button { 
                    padding: 12px 24px; 
                    background: #007bff; 
                    color: white; 
                    border: none; 
                    cursor: pointer;
                    border-radius: 4px;
                    font-weight: bold;
                    transition: background-color 0.3s;
                }
                button:hover {
                    background: #0056b3;
                }
                .message { 
                    margin: 15px 0; 
                    padding: 15px; 
                    border-radius: 8px;
                    max-width: 85%;
                }
                .user-message { 
                    background: #e3f2fd;
                    margin-left: auto;
                    border-bottom-right-radius: 2px;
                }
                .bot-message { 
                    background: #f8f9fa;
                    margin-right: auto;
                    border-bottom-left-radius: 2px;
                }
                pre { 
                    background: #f8f9fa; 
                    padding: 12px; 
                    border-radius: 4px; 
                    overflow-x: auto;
                    border: 1px solid #ddd;
                }
                code {
                    font-family: 'Consolas', 'Monaco', monospace;
                    font-size: 14px;
                }
                .message ul, .message ol {
                    padding-left: 20px;
                    margin: 10px 0;
                }
                .message li {
                    margin: 5px 0;
                }
                .message p {
                    margin: 10px 0;
                    line-height: 1.5;
                }
                .timestamp {
                    font-size: 12px;
                    color: #666;
                    margin-top: 5px;
                }
            </style>
        </head>
        <body>
            <h1>Code Assistant Chat</h1>
            <div id="chat-container"></div>
            <div id="input-container">
                <textarea id="message-input" placeholder="Type your message here... (Markdown supported)" rows="3"></textarea>
                <button onclick="sendMessage()">Send</button>
            </div>
            <script>
                // Initialize highlight.js
                hljs.highlightAll();
                
                // Configure marked for safe HTML
                marked.setOptions({
                    breaks: true,
                    gfm: true,
                    headerIds: false,
                    mangle: false,
                    sanitize: false,
                    highlight: function(code, language) {
                        if (language && hljs.getLanguage(language)) {
                            return hljs.highlight(code, { language: language }).value;
                        }
                        return hljs.highlightAuto(code).value;
                    }
                });

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
                    
                    // Add timestamp
                    const timestamp = new Date().toLocaleTimeString();
                    
                    // Parse markdown and handle code blocks
                    const formattedContent = marked.parse(content);
                    
                    messageDiv.innerHTML = `${formattedContent}<div class="timestamp">${timestamp}</div>`;
                    
                    container.appendChild(messageDiv);
                    container.scrollTop = container.scrollHeight;
                    
                    // Highlight code blocks in the new message
                    messageDiv.querySelectorAll('pre code').forEach((block) => {
                        hljs.highlightBlock(block);
                    });
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