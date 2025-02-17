import os
import time
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, HORIZONTAL
from PyPDF2 import PdfReader
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

# Secure API Key (Set in Environment Variables)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI LLM
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0.7,
    openai_api_key=OPENAI_API_KEY
)

def extract_text_from_pdf(file_path):
    """Extracts text from a PDF file."""
    try:
        with open(file_path, "rb") as pdf_data: #try to open file as binary data
            reader = PdfReader(pdf_data)
            text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
        return text or "No readable text found in PDF"
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read the PDF: {str(e)}")
        return None

def update_progress():
    """Simulates progress updates."""
    for value in range(0, 101, 20):  # Increment progress in steps of 20%
        progress["value"] = value
        root.update_idletasks()  # Keep UI responsive
        time.sleep(0.5)  # Simulate processing delay
    progress.grid_forget()  # Hide progress bar after completion

def summarize_file():
    """Handles file selection and summarizes the content."""
    file_path = filedialog.askopenfilename(title="Select a PDF File", filetypes=[("PDF Files", "*.pdf")])

    if not file_path:
        return  # User canceled file selection

    def real_summarize_file(): #Actual function that will summarize on another thread
        try:
            select_file_btn['state'] = 'disabled' #disable button
            progress.pack(pady=5)
            update_progress()  # Start progress updates

            text = extract_text_from_pdf(file_path)
            if text: #get summary from OpenAI using LangChain
                gpt_prompt = f"Summarize the following text:\n\n{text}"
                response = llm.invoke([HumanMessage(content=gpt_prompt)])
                summary = response.content

                # Display Summary in GUI
                summary_text.delete("1.0", tk.END)  # Clear previous text
                summary_text.insert(tk.END, summary)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to get AI summary: {str(e)}")

        progress.pack_forget()
        select_file_btn['state'] = 'normal'  # Re-enable button
    threading.Thread(target=real_summarize_file).start()

# Set up the GUI
root = tk.Tk()
root.title("PDF Summarizer")
root.geometry("500x400")

# File selection button
select_file_btn = tk.Button(root, text="Select PDF to Summarize", command=summarize_file)
select_file_btn.pack(pady=10)

#Progress bar
progress = ttk.Progressbar(root,
                       orient = HORIZONTAL,
                       length = 200,
                       mode = 'determinate'
                       )

# Text box for displaying the summary
summary_text = tk.Text(root, height=15, width=60, wrap="word")
summary_text.pack(pady=10)

# Run the application
root.mainloop()
