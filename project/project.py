import fitz  # PyMuPDF
import gradio as gr
import openai

openai.api_key = "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" 

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def answer_question(pdf_file, question):
    if not question:
        return "Please enter a question."
    
    text = extract_text_from_pdf(pdf_file)
    prompt = f"You are a helpful study assistant. Based on this content:\n\n{text[:3000]}\n\nAnswer this: {question}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.7
    )

    return response["choices"][0]["message"]["content"]

app = gr.Interface(
    fn=answer_question,
    inputs=[
        gr.File(label="Upload your PDF"),
        gr.Textbox(label="Ask a question about the document")
    ],
    outputs="text",
    title="📚 AI Study Buddy",
    description="Upload a PDF and ask anything about it. Powered by AI.",
    theme="default"
)

if __name__ == "__main__":
    app.launch()
