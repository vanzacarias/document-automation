import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from io import BytesIO


def add_text_to_pdf(input_pdf_path, output_pdf_path, text):
    # Read the existing PDF
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    # Create a new temporary PDF with the added text
    packet = BytesIO()
    c = canvas.Canvas(packet)
    
    # Add text to the temporary PDF (you can adjust the position)
    c.drawString(10, 10, text)  # Example coordinates (x=100, y=800)
    c.save()
    
    # Move the content of the canvas into a PDF
    packet.seek(0)
    new_pdf = PdfReader(packet)
    
    # Combine the original PDF with the new PDF
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        
        # Merge the content from the new PDF into the original page
        page.merge_page(new_pdf.pages[0])
        
        writer.add_page(page)
    
    # Write the final PDF to the output file
    with open(output_pdf_path, 'wb') as output_pdf:
        writer.write(output_pdf)

    messagebox.showinfo("Success", "Text added to PDF successfully!")


# Create the GUI
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        input_pdf_path.set(file_path)

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        output_pdf_path.set(file_path)

def process_pdf():
    text = text_entry.get()
    input_pdf = input_pdf_path.get()
    output_pdf = output_pdf_path.get()

    if not text:
        messagebox.showerror("Error", "Please enter text to add.")
        return
    if not input_pdf or not output_pdf:
        messagebox.showerror("Error", "Please select an input and output PDF file.")
        return
    
    add_text_to_pdf(input_pdf, output_pdf, text)


# Set up the main window
window = tk.Tk()
window.title("PDF Text Inserter")
window.geometry("400x300")

# Variables to store paths
input_pdf_path = tk.StringVar()
output_pdf_path = tk.StringVar()

# Create the widgets
tk.Label(window, text="Text to add:").pack(pady=10)
text_entry = tk.Entry(window, width=50)
text_entry.pack(pady=5)

tk.Button(window, text="Select Input PDF", command=open_file).pack(pady=10)
tk.Label(window, textvariable=input_pdf_path).pack(pady=5)

tk.Button(window, text="Select Output PDF", command=save_file).pack(pady=10)
tk.Label(window, textvariable=output_pdf_path).pack(pady=5)

tk.Button(window, text="Add Text to PDF", command=process_pdf).pack(pady=20)

# Start the GUI event loop
window.mainloop()
