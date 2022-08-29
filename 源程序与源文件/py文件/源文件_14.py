import pdfplumber
import pandas as pd

def read_pdf(read_path, save_path):
    pdf = pdfplumber.open(read_path)
    excel= pd.DataFrame()
    for page in pdf.pages:
        table = page.extract_table()
        print(table)
        df_detail = pd.DataFrame(table[1:], columns=table[0])
        excel = pd.concat([df_detail, excel], ignore_index=True)
    excel.dropna(axis=1, how='all', inplace=True)
    excel.columns = ['院系', '专业', '学习方式', '学位类别', '报考数', '录取数','复试线']
    excel.to_excel(excel_writer=save_path, index=False, encoding='utf-8')

read_path = r'华东师范大学2021报录情况.pdf'
save_path = r'华东师范大学2021报录情况.xlsx'
read_pdf(read_path, save_path)

