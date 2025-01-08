# AI Code Assistant & Productivity Bot

An intelligent programming assistant powered by OpenAI GPT that helps with code analysis, debugging, and productivity tracking. The assistant can detect multiple programming languages, provide code explanations, and suggest best practices.

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green)
![License](https://img.shields.io/badge/license-MIT-blue)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5-orange)

## Overview

This AI-powered Code Assistant helps developers with:
- Code analysis and debugging
- Best practices recommendations
- Multi-language support
- Interactive coding assistance
- Productivity tracking (coming soon)

## Features

- 🔍 **Language Detection**: Automatically identifies Python, JavaScript, Java, and C++
- 💡 **Code Analysis**: Provides detailed code explanations and suggestions
- 🐛 **Debugging Help**: Identifies potential issues and offers solutions
- 📝 **Best Practices**: Recommends coding standards and patterns
- 🎯 **Context-Aware**: Understands code context for better assistance
- 🌐 **Web Interface**: Easy-to-use chat interface
- 📊 **API Documentation**: Complete Swagger/ReDoc documentation

## Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- OpenAI API key
- Git (for cloning the repository)

## Quick Start

1. **Clone the Repository**bash
git clone https://github.com/yourusername/code-assistant.git
cd code-assistant

2. **Set Up Python Environment**

For Windows:
bash
python -m venv venv
venv\Scripts\activate


For macOS/Linux:
bash:README.md
python -m venv venv
source venv/bin/activate


3. **Install Dependencies**
bash:README.md
pip install -r requirements.txt


4. **Configure Environment**

Create a `.env` file in the project root:
env
OPENAI_API_KEY=your_openai_api_key_here


5. **Start the Application**
bash
python run.py


## Accessing the Application

After starting, access these URLs:
- 🌐 Web Interface: http://localhost:8000/
- 📚 Swagger Docs: http://localhost:8000/docs
- 📖 ReDoc: http://localhost:8000/redoc

## API Usage Examples

### Using curl
bash
curl -X POST "http://localhost:8000/api/chat" \
-H "Content-Type: application/json" \
-d '{
"message": "How do I write a hello world program in Python?",
"context": {
"code": "print(\"Hello\")"
}
}'


### Using Python requests
python
import requests
response = requests.post(
"http://localhost:8000/api/chat",
json={
"message": "How do I write a hello world program in Python?",
"context": {"code": "print('Hello')"}
}
)
print(response.json())


## Project Structure
project_root/
│
├── backend/
│ ├── app/
│ │ ├── api/
│ │ ├── core/
│ │ │ ├── config.py # Configuration settings
│ │ │ └── init.py
│ │ ├── models/
│ │ ├── services/
│ │ │ ├── chat_service.py # Main chat service
│ │ │ └── init.py
│ │ └── main.py # FastAPI application
│ └── tests/
│ ├── test_chat_service.py
│ └── init.py
├── requirements.txt # Python dependencies
├── run.py # Application entry point
└── .env # Environment variables


## Development and Testing

### Running Tests
bash
pytest backend/tests/ -v


### Development Setup
1. Fork the repository
2. Create a development branch
3. Install development dependencies
4. Run tests before submitting PR

## Troubleshooting

### Common Issues and Solutions

1. **Import Errors**
   - Run from project root directory
   - Verify all `__init__.py` files exist
   - Check Python path in `run.py`

2. **API Key Issues**
   - Verify OpenAI API key in `.env`
   - Check API key permissions
   - Ensure `.env` file is in root directory

3. **Port Conflicts**
   - Default port is 8000
   - Change port in `run.py` if needed
   - Check for other services using port 8000

## Roadmap

See [ROADMAP.md](roadmap.md) for detailed development plans including:
- Enhanced code analysis
- Productivity tools integration
- Documentation assistant
- Team collaboration features
- Database integration

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Security

- Never commit `.env` file
- Keep dependencies updated
- Use environment variables for sensitive data
- Regular security audits recommended

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📫 Open an issue for bugs
- 💡 Feature requests welcome
- 📚 Check documentation first
- 🤝 Community contributions encouraged

## Acknowledgments

- OpenAI for GPT API
- FastAPI framework
- All contributors

---
Made with ❤️ by Vijay
