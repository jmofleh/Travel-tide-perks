import gradio as gr
import pandas as pd

# 1. Load your data (using the path from your error message)
def load_data():
    df = pd.read_csv("data/processed/travel_tide.csv")
    return df.head()

# 2. Define the function that does the "work"
def greet(name):
    return f"Hello {name}! Here is a preview of the Travel Tide data."

# 3. Create the Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("# Travel Tide Perks Analysis")
    
    name_input = gr.Textbox(label="Enter your Name")
    output_text = gr.Textbox(label="Greeting")
    submit_btn = gr.Button("Run Analysis")
    
    # Simple table display
    data_display = gr.DataFrame(value=load_data())
    
    submit_btn.click(fn=greet, inputs=name_input, outputs=output_text)

# 4. Launch the app
if __name__ == "__main__":
    demo.launch()
