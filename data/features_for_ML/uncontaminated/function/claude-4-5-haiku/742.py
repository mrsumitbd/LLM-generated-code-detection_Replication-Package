from flask import Flask, render_template_string
from anthropic import Anthropic

def create_app():
    app = Flask(__name__)
    client = Anthropic()
    
    # Store conversation history per session
    conversation_history = {}
    
    @app.route('/')
    def index():
        html_template = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Claude Chat</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f5f5f5;
                }
                .chat-container {
                    background-color: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    padding: 20px;
                    height: 500px;
                    display: flex;
                    flex-direction: column;
                }
                .messages {
                    flex: 1;
                    overflow-y: auto;
                    margin-bottom: 20px;
                    border: 1px solid #ddd;
                    padding: 10px;
                    border-radius: 4px;
                }
                .message {
                    margin-bottom: 10px;
                    padding: 10px;
                    border-radius: 4px;
                }
                .user-message {
                    background-color: #e3f2fd;
                    text-align: right;
                }
                .assistant-message {
                    background-color: #f5f5f5;
                }
                .input-area {
                    display: flex;
                    gap: 10px;
                }
                input {
                    flex: 1;
                    padding: 10px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    font-size: 14px;
                }
                button {
                    padding: 10px 20px;
                    background-color: #1976d2;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    font-size: 14px;
                }
                button:hover {
                    background-color: #1565c0;
                }
                .clear-btn {
                    background-color: #d32f2f;
                }
                .clear-btn:hover {
                    background-color: #c62828;
                }
            </style>
        </head>
        <body>
            <h1>Claude Chat</h1>
            <div class="chat-container">
                <div class="messages" id="messages"></div>
                <div class="input-area">
                    <input type="text" id="userInput" placeholder="Type your message..." />
                    <button onclick="sendMessage()">Send</button>
                    <button class="clear-btn" onclick="clearChat()">Clear</button>
                </div>
            </div>
            
            <script>
                function sendMessage() {
                    const input = document.getElementById('userInput');
                    const message = input.value.trim();
                    
                    if (!message) return;
                    
                    // Add user message to display
                    addMessageToDisplay(message, 'user');
                    input.value = '';
                    
                    // Send to server
                    fetch('/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ message: message })
                    })
                    .then(response => response.json())
                    .then(data => {
                        addMessageToDisplay(data.response, 'assistant');
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        addMessageToDisplay('Error: Could not get response', 'assistant');
                    });
                }
                
                function addMessageToDisplay(message, sender) {
                    const messagesDiv = document.getElementById('messages');
                    const messageDiv = document.createElement('div');
                    messageDiv.className = 'message ' + sender + '-message';
                    messageDiv.textContent = message;
                    messagesDiv.appendChild(messageDiv);
                    messagesDiv.scrollTop = messagesDiv.scrollHeight;
                }
                
                function clearChat() {
                    fetch('/clear', { method: 'POST' })
                    .then(() => {
                        document.getElementById('messages').innerHTML = '';
                    });
                }
                
                document.getElementById('userInput').addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        sendMessage();
                    }
                });
            </script>
        </body>
        </html>
        '''
        return render_template_string(html_template)
    
    @app.route('/chat', methods=['POST'])
    def chat():
        from flask import request, jsonify
        
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'response': 'Please enter a message.'})
        
        # Get or create conversation history for this session
        session_id = request.remote_addr
        if session_id not in conversation_history:
            conversation_history[session_id] = []
        
        # Add user message to history
        conversation_history[session_id].append({
            "role": "user",
            "content": user_message
        })
        
        # Get response from Claude
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=conversation_history[session_id]
        )
        
        assistant_message = response.content[0].text
        
        # Add assistant response to history
        conversation_history[session_id].append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return jsonify({'response': assistant_message})
    
    @app.route('/clear', methods=['POST'])
    def clear():
        from flask import request, jsonify
        
        session_id = request.remote_addr
        if session_id in conversation_history:
            conversation_history[session_id] = []
        
        return jsonify({'status': 'cleared'})
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)