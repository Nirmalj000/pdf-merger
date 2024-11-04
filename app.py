from flask import Flask, render_template, request, send_file
import PyPDF2
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure the upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def merge_pdfs(pdf_paths, output_path):
    pdf_writer = PyPDF2.PdfWriter()

    # Loop through each PDF file path and add all pages to the writer
    for pdf_path in pdf_paths:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page in pdf_reader.pages:
                pdf_writer.add_page(page)

    # Write the merged PDF to the output file
    with open(output_path, 'wb') as output_file:
        pdf_writer.write(output_file)

@app.route('/')
def upload_files():
    return render_template('upload.html')

@app.route('/merge', methods=['POST'])
def merge():
    files = request.files.getlist('pdfs')
    if not files:
        return "No PDF files uploaded.", 400

    # Save each uploaded file to the upload folder and collect the paths in the given order
    pdf_paths = []
    for pdf in files:
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf.filename)
        pdf.save(pdf_path)
        pdf_paths.append(pdf_path)

    # Define output path
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'merged_output.pdf')

    # Merge the PDFs
    merge_pdfs(pdf_paths, output_path)

    # Send the merged PDF file to be opened in a new tab
    return send_file(output_path, as_attachment=False)

if __name__ == '__main__':
    app.run(debug=True)
