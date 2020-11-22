# modulos importados
import PyPDF2
# import fitz
import os
# import re

# variaveis
root_dir = r"/home/tiagomurilo/Documentos/pdfFinanceiro/original"
extract_to = r"/home/tiagomurilo/Documentos/pdfFinanceiro/ajustado"


# função que extrai documentos das paginas
def split_pdf_pages(root_directory, extract_to_folder):
    # pegando diretório e arquivos
    for root, dirs, files in os.walk(root_directory):
        # para cada arquivo se busca o nome e extenção
        for filename in files:
            basename, extension = os.path.splitext(filename)
            # verifica se arquivo é PDF
            if extension == ".pdf":
                # referencia a pasta com o nome do novo arquivo
                fullpath = root + "/" + basename + extension
                # abre o pdf no modo leitura
                opened_pdf = PyPDF2.PdfFileReader(open(fullpath, "rb"))
                # conta paginas achadas no pdf
                for i in range(opened_pdf.getNumPages()):
                    # write the page to a new pdf
                    output = PyPDF2.PdfFileWriter()
                    output.addPage(opened_pdf.getPage(i))
                    
                    with open(extract_to_folder + "/" + basename + " - " + str(i + 1) + ".pdf", "wb") as output_pdf:
                        output.write(output_pdf)


# use the two functions
split_pdf_pages(root_dir, extract_to)