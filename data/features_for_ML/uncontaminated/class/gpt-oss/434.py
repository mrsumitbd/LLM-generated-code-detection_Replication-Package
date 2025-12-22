import os
import sys
import argparse
import openai
import gradio as gr


class MedicalCoder:
    """
    A class to provide AI-powered medical coding for ICD-10 and CPT codes.
    """

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        openai.api_key = self.api_key

    def start_gradio(self):
        def _ask(file_obj):
            if file_obj is None:
                return "No file uploaded."
            content = file_obj.read().decode("utf-8")
            return self.ask(content)

        iface = gr.Interface(
            fn=_ask,
            inputs=gr.File(label="Upload Clinical Notes"),
            outputs=gr.Textbox(label="ICD-10 & CPT Codes"),
            title="Medical Coding Assistant",
            description="Upload a clinical notes file and receive ICD-10 and CPT codes.",
        )
        iface.launch()

    def run_cli(self):
        parser = argparse.ArgumentParser(description="Medical Coding CLI")
        parser.add_argument(
            "file",
            type=str,
            help="Path to the clinical notes file (text or PDF).",
        )
        args = parser.parse_args()
        if not os.path.isfile(args.file):
            print(f"File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        with open(args.file, "rb") as f:
            content = f.read().decode("utf-8", errors="ignore")
        result = self.ask(content)
        print(result)

    def ask(self, file_content, **kwargs):
        """
        Generate ICD-10 and CPT codes for the given clinical notes.

        Parameters:
            file_content (str): The content of the clinical notes.
            **kwargs: Additional arguments for the OpenAI API.

        Returns:
            str: The AI-generated ICD-10 and CPT codes.
        """
        prompt = (
            "You are a medical coder. Based on the following clinical notes, "
            "provide a list of ICD-10 diagnosis codes and CPT procedure codes. "
            "Return the codes in a clear, numbered format.\n\n"
            f"Clinical Notes:\n{file_content}\n\n"
            "ICD-10 Codes:\n"
            "CPT Codes:\n"
        )
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=500,
                **kwargs,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating codes: {e}"