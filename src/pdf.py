from fpdf import FPDF
titulo = "Evolución de las temperaturas en el mundo"

def creaPDF():
    pdf = FPDF('L','mm','A4')
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(190, 10, f"{titulo}",1,1,'C')
    pdf.set_font('Courier', '',10)
    pdf.cell(190, 10, 'Últimos diez años de evolución de las temperaturas.','',1,'C')
    pdf.ln(6)
    pdf.text(10,30,'En el primer gráfico podemos observar la evolución mundial de las temperaturas en los últimos diez años.')
    pdf.ln(50)
    pdf.image('output/avgtemperatureEarth.png',x=70, y=50, w=100)
    pdf.set_font('Courier', '',13)
    pdf.cell(90,50,'¿Y si queremos ver la evolución de las temperaturas en una sola ciudad, la década pasada?','',1)
    pdf.set_font('Courier', '',10)
    pdf.image('output/avgtempplot.png',x=70, y=130, w=100)
    pdf.cell(150,90,'Por otro lado, el  siguiente gráfico pinta la evolución de las precipitaciones en Madrid :','',1)
    pdf.image('output/RainChange.png',x=70, y=100, w=100)
    pdf.output("file.pdf")
    pdf.output("src/report.pdf", "F")
   



