import gradio as gr

def check_input_image(input_image):
    if input_image is None:
        raise gr.Error("No image uploaded!")