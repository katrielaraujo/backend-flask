from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO


def generate_sales_pdf(sales, start_data, end_date):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle(f"Vendas de {start_data} a {end_date}")

    pdf.drawString(100, 750, f"Vendas de {start_data} a {end_date}")
    pdf.drawString(50, 700, "ID")
    pdf.drawString(100, 700, "Nome do Cliente")
    pdf.drawString(250, 700, "Produto")
    pdf.drawString(400, 700, "Valor")
    pdf.drawString(500, 700, "Data")

    y = 650
    for sale in sales:
        pdf.drawString(50, y, str(sale['id']))
        pdf.drawString(100, y, sale['nome_cliente'])
        pdf.drawString(250, y, sale['produto'])
        pdf.drawString(400, y, str(sale['valor']))
        pdf.drawString(500, y, sale['data_venda'])
        y -= 30

    pdf.showPage()
    pdf.save()
    buffer.seek(0)

    return buffer

