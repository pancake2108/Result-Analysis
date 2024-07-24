from flask import Flask, request, send_file
import pandas as pd
import pdfplumber
import openpyxl
from io import BytesIO

app = Flask(__name__)

def pdf_to_excel(pdf_path):
    # Extract data from PDF and convert to Excel
    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()
        # Parse text and convert to DataFrame
        data = parse_pdf_text_to_dataframe(text)
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            data.to_excel(writer, index=False)
        return excel_buffer

def parse_pdf_text_to_dataframe(text):
    # Custom function to parse text and convert to DataFrame
    # Implement parsing logic here
    data = []  # Parse text and fill this list
    columns = ["Student Name", "Subject", "Marks"]  # Example columns
    df = pd.DataFrame(data, columns=columns)
    return df

def analyze_results(df):
    # Perform data analysis
    toppers = df.nlargest(10, 'Marks')
    subject_toppers = df.groupby('Subject').apply(lambda x: x.nlargest(10, 'Marks')).reset_index(drop=True)
    return toppers, subject_toppers

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file.filename.endswith('.pdf'):
        pdf_path = file
        excel_buffer = pdf_to_excel(pdf_path)
        excel_buffer.seek(0)
        df = pd.read_excel(excel_buffer)
        toppers, subject_toppers = analyze_results(df)
        output_buffer = BytesIO()
        with pd.ExcelWriter(output_buffer, engine='openpyxl') as writer:
            toppers.to_excel(writer, sheet_name='Top 10 Toppers', index=False)
            subject_toppers.to_excel(writer, sheet_name='Subject Wise Toppers', index=False)
        output_buffer.seek(0)
        return send_file(output_buffer, as_attachment=True, download_name='result_analysis.xlsx')
    else:
        return "Invalid file format", 400

if __name__ == '__main__':
    app.run(debug=True)
