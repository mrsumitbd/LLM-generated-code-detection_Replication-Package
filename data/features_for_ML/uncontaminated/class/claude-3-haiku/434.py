import gradio as gr
import os
import openai

class MedicalCoder:
    """
    A class to provide AI-powered medical coding for ICD-10 and CPT codes.
    """

    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def start_gradio(self):
        demo = gr.Interface(
            fn=self.ask,
            inputs=[
                gr.File(label="Upload Medical Report"),
                gr.Checkbox(label="Include ICD-10 Codes"),
                gr.Checkbox(label="Include CPT Codes"),
            ],
            outputs=[
                gr.Textbox(label="ICD-10 Codes"),
                gr.Textbox(label="CPT Codes"),
            ],
            title="AI-Powered Medical Coder",
            description="Upload a medical report and get the corresponding ICD-10 and CPT codes.",
        )
        demo.launch()

    def run_cli(self):
        file_path = input("Enter the path to the medical report file: ")
        include_icd10 = input("Include ICD-10 Codes? (y/n) ").lower() == "y"
        include_cpt = input("Include CPT Codes? (y/n) ").lower() == "y"
        icd10_codes, cpt_codes = self.ask(file_path, include_icd10=include_icd10, include_cpt=include_cpt)
        print("ICD-10 Codes:", icd10_codes)
        print("CPT Codes:", cpt_codes)

    def ask(self, file_path, **kwargs):
        with open(file_path, "r") as file:
            medical_report = file.read()

        prompt = f"Provide the relevant ICD-10 and CPT codes for the following medical report:\n\n{medical_report}\n\n"
        if kwargs.get("include_icd10", True):
            prompt += "ICD-10 Codes:"
        if kwargs.get("include_cpt", True):
            prompt += " CPT Codes:"
        prompt += "\n"

        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
        )

        output = response.choices[0].text.strip()
        icd10_codes, cpt_codes = output.split("\n")
        return icd10_codes, cpt_codes