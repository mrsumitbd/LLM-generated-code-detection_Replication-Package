import os
import json
import gradio as gr
from anthropic import Anthropic

class MedicalCoder:
    """
    A class to provide AI-powered medical coding for ICD-10 and CPT codes.
    """

    def __init__(self):
        self.client = Anthropic()
        self.conversation_history = []
        self.system_prompt = """You are an expert medical coder with extensive knowledge of ICD-10 and CPT codes. 
Your role is to help healthcare professionals accurately code medical diagnoses and procedures.

When provided with medical documentation, you should:
1. Identify the relevant diagnoses and procedures
2. Suggest appropriate ICD-10 codes for diagnoses
3. Suggest appropriate CPT codes for procedures
4. Provide the code descriptions and any relevant notes
5. Explain your coding decisions

Always be thorough and accurate, as medical coding directly impacts billing and patient records.
Format your responses clearly with:
- ICD-10 Codes: [list codes with descriptions]
- CPT Codes: [list codes with descriptions]
- Notes: [any relevant coding notes or considerations]"""

    def start_gradio(self):
        """Start the Gradio interface for the medical coder."""
        def process_input(user_message, history):
            self.conversation_history.append({
                "role": "user",
                "content": user_message
            })
            
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=8096,
                system=self.system_prompt,
                messages=self.conversation_history
            )
            
            assistant_message = response.content[0].text
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message

        def clear_history():
            self.conversation_history = []
            return []

        with gr.Blocks(title="Medical Coder") as demo:
            gr.Markdown("# Medical Coder - ICD-10 and CPT Code Assistant")
            gr.Markdown("Upload medical documents or describe patient cases to get coding suggestions.")
            
            with gr.Row():
                with gr.Column():
                    file_input = gr.File(label="Upload Medical Document", file_types=[".txt", ".pdf", ".docx"])
                    text_input = gr.Textbox(
                        label="Or describe the medical case",
                        placeholder="Enter patient diagnosis, procedures, or medical documentation...",
                        lines=5
                    )
                    submit_btn = gr.Button("Get Coding Suggestions", variant="primary")
                    clear_btn = gr.Button("Clear History")
                
                with gr.Column():
                    output = gr.Textbox(
                        label="Coding Suggestions",
                        lines=10,
                        interactive=False
                    )
            
            chat_history = gr.Chatbot(label="Conversation History")
            
            def handle_submission(file, text):
                user_input = text
                if file:
                    try:
                        if file.name.endswith('.txt'):
                            with open(file.name, 'r') as f:
                                file_content = f.read()
                        else:
                            file_content = f"[File uploaded: {file.name}]"
                        user_input = f"Medical Document Content:\n{file_content}\n\nPlease provide coding suggestions for this document."
                    except Exception as e:
                        user_input = f"Error reading file: {str(e)}. Please describe the case instead."
                
                if not user_input.strip():
                    return "Please enter a medical case description or upload a document.", chat_history.value if hasattr(chat_history, 'value') else []
                
                response = process_input(user_input, [])
                
                # Update chat history
                history = []
                for msg in self.conversation_history:
                    if msg["role"] == "user":
                        history.append([msg["content"], None])
                    else:
                        if history and history[-1][1] is None:
                            history[-1][1] = msg["content"]
                        else:
                            history.append([None, msg["content"]])
                
                return response, history
            
            submit_btn.click(
                handle_submission,
                inputs=[file_input, text_input],
                outputs=[output, chat_history]
            )
            
            clear_btn.click(
                clear_history,
                outputs=[chat_history]
            )
        
        demo.launch()

    def run_cli(self):
        """Run the medical coder in CLI mode."""
        print("Medical Coder - ICD-10 and CPT Code Assistant")
        print("=" * 50)
        print("Enter medical cases or descriptions to get coding suggestions.")
        print("Type 'quit' to exit, 'clear' to clear history, or 'file <path>' to load a file.")
        print("=" * 50)
        
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() == 'quit':
                print("Goodbye!")
                break
            
            if user_input.lower() == 'clear':
                self.conversation_history = []
                print("Conversation history cleared.")
                continue
            
            if user_input.lower().startswith('file '):
                file_path = user_input[5:].strip()
                try:
                    with open(file_path, 'r') as f:
                        file_content = f.read()
                    user_input = f"Medical Document Content:\n{file_content}\n\nPlease provide coding suggestions for this document."
                except FileNotFoundError:
                    print(f"File not found: {file_path}")
                    continue
                except Exception as e:
                    print(f"Error reading file: {str(e)}")
                    continue
            
            if not user_input:
                continue
            
            self.conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=8096,
                system=self.system_prompt,
                messages=self.conversation_history
            )
            
            assistant_message = response.content[0].text
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            print(f"\nAssistant: {assistant_message}")

    def ask(self, file_path, **kwargs):
        """
        Ask the medical coder to process a file and return coding suggestions.
        
        Args:
            file_path: Path to the medical document file
            **kwargs: Additional arguments (e.g., query for specific coding needs)
        
        Returns:
            str: The coding suggestions from the AI
        """
        try:
            with open(file_path, 'r') as f:
                file_content = f.read()
        except FileNotFoundError:
            return f"Error: File not found at {file_path}"
        except Exception as e:
            return f"Error reading file: {str(e)}"
        
        query = kwargs.get('query', '')
        user_message = f"Medical Document Content:\n{file_content}"
        
        if query:
            user_message += f"\n\nSpecific coding request: {query}"
        else:
            user_message += "\n\nPlease provide comprehensive coding suggestions for this document."
        
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=8096,
            system=self.system_prompt,
            messages=self.conversation_history
        )
        
        assistant_message = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return assistant_message


if __name__ == "__main__":
    import sys
    
    coder = MedicalCoder()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "gradio":
            coder.start_gradio()
        elif sys.argv[1] == "file" and len(sys.argv) > 2:
            result = coder.ask(sys.argv[2])
            print(result)
        else:
            print("Usage: python solution.py [gradio|file <path>]")
            print("Or run without arguments for CLI mode")
    else:
        coder.run_cli()