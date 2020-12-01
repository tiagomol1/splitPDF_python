# modulos importados
import PyPDF2
import os
import fitz

# variaveis
root_dir = r"/home/tiagomurilo/Documentos/pdfFinanceiro/original"
extract_to_boletos = r"/home/tiagomurilo/Documentos/pdfFinanceiro/boletos"
extract_to_darf = r"/home/tiagomurilo/Documentos/pdfFinanceiro/darf"
extract_to_nfe = r"/home/tiagomurilo/Documentos/pdfFinanceiro/nfe"

def split_pdf_pages():
    # pegando diretório e arquivos
    for root, dirs, files in os.walk(root_dir):
        # para cada arquivo se busca o nome e extenção
        for filename in files:
            directory = r"/home/tiagomurilo/Documentos/pdfFinanceiro/ajustado"
            basename, extension = os.path.splitext(filename)

            # verifica se arquivo é PDF
            if extension == ".pdf":
                # referencia a pasta com o nome do novo arquivo
                fullpath = root + "/" + basename + extension
                pdf_file_obj = fitz.Document(fullpath)
                pdf_reader = pdf_file_obj.loadPage(0)
                pdf_text = str(pdf_reader.getText("text"))

                if pdf_text.find("BRADESCO") != -1:
                    directory = extract_to_boletos
                elif pdf_text.find("Esta NF-em foi gerada com fundamento na Lei Complementar Municipal n. 286, de 21") != -1:
                    directory = extract_to_nfe
                elif pdf_text.find("Itaú Unibanco") != -1:
                    directory = extract_to_boletos
                elif pdf_text.find("BANRISUL") != -1:
                    directory = extract_to_boletos
                elif pdf_text.find("PIS / COFINS / CSLL") != -1:
                    directory = extract_to_darf

                # abre o pdf no modo leitura
                opened_pdf = PyPDF2.PdfFileReader(open(fullpath, "rb"))
                # conta paginas achadas no pdf
                for i in range(opened_pdf.getNumPages()):
                    # write the page to a new pdf
                    output = PyPDF2.PdfFileWriter()
                    output.addPage(opened_pdf.getPage(i))

                    with open(directory + "/" + basename + " - " + str(i + 1) + ".pdf", "wb") as output_pdf:
                        output.write(output_pdf)

def rename_identifyClient_boletos():
    archives = []
    data = []

    for root, dirs, files in os.walk(extract_to_boletos):
        for filename in files:
            basename, extension = os.path.splitext(filename)

            archives.append(extract_to_boletos + "/" + basename + "" + extension)

    for archive in archives:
        pdf_file_obj = fitz.Document(archive)
        pdf_reader = pdf_file_obj.loadPage(0)
        pdf_text = str(pdf_reader.getText("text"))

        if pdf_text.find("BRADESCO") != -1:
            nfe = pdf_text.split('APÓS 10 DIAS VENCIDO SUJEITO A ENVIO A CARTÓRIO')[3].split('\n')[5].split('\n')[0].replace('/', ' ')
            clientData = pdf_text.split("Pagador")[3].split("\n")[12].replace('-', '')
            clientCnpj = clientData.split('  ')[0].replace('.', '').replace('/', '')
            clientCode = clientData.split('  ')[1]
            clientNameAdjust = clientData.replace('&', 'E').split('  ')[2].split(' ')
            if clientNameAdjust[1] == "da" or clientNameAdjust[1] == "DA" or clientNameAdjust[1] == "de" or clientNameAdjust[1] == "DE" or clientNameAdjust[1] == "E" or clientNameAdjust[1] == "e":
                    clientNameAdjust.remove(clientNameAdjust[1])
            clientName = str(clientNameAdjust[0] + " " +clientNameAdjust[1]).replace('.', '')
            metaName = pdf_text.split("Pagador")[3].split("\n")[2].replace('-', '')
            searchMetaCnpj = pdf_text.split("Pagável Preferencialmente na rede Bradesco ou no Bradesco expresso")[3].split('APÓS 10 DIAS VENCIDO SUJEITO A ENVIO A CARTÓRIO')[0].split("CPF/CNPJ do Sacado\n")[2].split('\n')[0]
            metaCnpj = searchMetaCnpj.replace('.', '').replace('/', '').replace('-', '')
            processDate = pdf_text.split("Data do Documento")[1].split("\n")[1][3:10].replace('/', '-')

            os.rename(archive, extract_to_boletos + "/" + clientName + " - NF " + nfe + " - (Boleto Bradesco)" + extension)
            data.append({
                "nfe": nfe,
                "processDate": processDate,
                "clientCnpj": clientCnpj,
                "clientCode": clientCode,
                "clientName": clientName,
                "metaCnpj": metaCnpj,
                "metaName": metaName,
                "type": "Boleto",
                "archive": extract_to_boletos + "/" + clientName + " - NF " + nfe + " - (Boleto Bradesco)" + extension
            })

        if pdf_text.find("Itaú Unibanco") != -1:
            nfe = pdf_text.split("Valor do Documento\n")[2].split("\n")[4].replace('/', ' ')
            clientNameAdjust = pdf_text.split("Pagador\n")[1].split("\n")[0].replace('.', '').replace('&', 'E').split(' ')
            if clientNameAdjust[1] == "da" or clientNameAdjust[1] == "DA" or clientNameAdjust[1] == "de" or clientNameAdjust[1] == "DE" or clientNameAdjust[1] == "E" or clientNameAdjust[1] == "e":
                clientNameAdjust.remove(clientNameAdjust[1])
            clientName = clientNameAdjust[0] + " - " + clientNameAdjust[1]
            clientCnpj = pdf_text.split("Benef iciário")[2].split("\n")[1].replace('.', '').replace('/', '').replace('-', '')
            clientCode = '-'
            metaName = pdf_text.split("APÓS 10 DIAS VENCIDO SUJEITO A ENVIO A CARTÓRIO")[1].split("\n")[1].split("-")[0]
            metaCnpj = pdf_text.split("APÓS 10 DIAS VENCIDO SUJEITO A ENVIO A CARTÓRIO")[1].split("\n")[1].split("CNPJ: ")[1].replace('.', '').replace('/', '').replace('-', '')
            processDate = pdf_text.split("Número do Documento\n")[1].split("\n")[2][3:10].replace('/', '-')

            os.rename(archive, extract_to_boletos + "/" + clientName + " - NF " + nfe + " - (Boleto Itau)" + extension)
            data.append({
                "nfe": nfe,
                "processDate": processDate,
                "clientCnpj": clientCnpj,
                "clientCode": clientCode,
                "clientName": clientName,
                "metaCnpj": metaCnpj,
                "metaName": metaName,
                "type": "Boleto",
                "archive": extract_to_boletos + "/" + clientName + " - NF " + nfe + " - (Boleto Itau)" + extension
            })

        if pdf_text.find("BANRISUL") != -1:
            nfe = pdf_text.split('Número do Documento\n')[1].split('\n')[0].replace('/', ' ')

            processDate = pdf_text.split('Data do Processamento\n')[1].split('\n')[0][3:10].replace('/', '-')
            clientNameAdjust = pdf_text.split('Pagador\n')[1].split('\n')[0].replace('-', '').replace('&', '').replace('.', '').split(' ')
            if clientNameAdjust[1] == "da" or clientNameAdjust[1] == "DA" or clientNameAdjust[1] == "de" or clientNameAdjust[1] == "DE" or clientNameAdjust[1] == "E" or clientNameAdjust[1] == "e" or clientNameAdjust[1] == "do" or clientNameAdjust[1] == "DO":
                clientNameAdjust.remove(clientNameAdjust[1])
            clientName = clientNameAdjust[0] + " " + clientNameAdjust[1]
            clientCnpj = pdf_text.split('Pagador\n')[1].split('\n')[2].replace('.', '').replace('/', '').replace('-', '')
            clientCode = '-'
            metaCnpj = pdf_text.split('CPF/CNPJ\n ')[1].split('\n')[0].replace('.', '').replace('/', '').replace('-', '')
            metaName = pdf_text.split('CPF/CNPJ - \n')[2].split('\n')[3].split(" - ")[0]

            os.rename(archive, extract_to_boletos + "/" + clientName + " - NF " + nfe + " - (Boleto Banrisul)" + extension)
            data.append({
                "nfe": nfe,
                "processDate": processDate,
                "clientCnpj": clientCnpj,
                "clientCode": clientCode,
                "clientName": clientName,
                "metaCnpj": metaCnpj,
                "metaName": metaName,
                "type": "Boleto",
                "archive": extract_to_boletos + "/" + clientName + " - NF " + nfe + " - (Boleto Banrisul)" + extension
            })

    return data

def rename_identifyClient_nfe():
    archives = []
    data = []

    for root, dirs, files in os.walk(extract_to_nfe):
        for filename in files:
            basename, extension = os.path.splitext(filename)
            archives.append(extract_to_nfe + "/" + basename + "" + extension)

    for archive in archives:

        pdf_file_obj = fitz.Document(archive)
        pdf_reader = pdf_file_obj.loadPage(0)
        pdf_text = str(pdf_reader.getText("text"))

        if(pdf_text.find("Número da NF-em ") != -1):
            nfe = pdf_text.split("Número da NF-em ")[1].split(" ")[0].split("\n")[1]
            clientCode = pdf_text.split("TOMADOR DE SERVIÇO")[1].split("Nome/Razão Social:\n")[1].split("-")[0]
            clientName = pdf_text.split("TOMADOR DE SERVIÇO")[1].split("Nome/Razão Social:\n")[1].split("-")[1].split("\n")[0].replace('.', '').replace('&', 'E')
            clientCnpj = pdf_text.split("TOMADOR DE SERVIÇO")[1].split("CPF/CNPJ:\n")[1].split('\n')[0].replace(".", "").replace('-', '').replace('/', '')
            metaCnpj = pdf_text.split("PRESTADOR DE SERVIÇOS")[1].split("CPF/CNPJ:\n")[1].split('\n')[0].replace(".", "").replace('-', '').replace('/', '')
            metaName = pdf_text.split("PRESTADOR DE SERVIÇOS")[1].split("Razão Social:\n")[1].split('\n')[0].replace('.', '').replace('&', 'E')
            clientNameAdjust = clientName.split(' ')
            if(clientNameAdjust[1] == "da" or clientNameAdjust[1] == "DA" or clientNameAdjust[1] == "de" or clientNameAdjust[1] == "DE" or clientNameAdjust[1] == "E" or clientNameAdjust[1] == "e"):
                clientNameAdjust.remove(clientNameAdjust[1])
            clientName = clientNameAdjust[0] + " " + clientNameAdjust[1]
            processDate = pdf_text.split('Data e Hora de Emissão')[0].split('\n')[0][3:10].replace('/', '-')

            os.rename(archive, extract_to_nfe + "/" + clientName + " - NF " + nfe + " - (NFe )" + extension)
            data.append({
                "nfe": nfe,
                "processDate": processDate,
                "clientCnpj": clientCnpj,
                "clientCode": clientCode,
                "clientName": clientName,
                "metaCnpj": metaCnpj,
                "metaName": metaName,
                "type": "NFe",
                "archive": extract_to_nfe + "/" + clientName + " - NF " + nfe + " - (NFe )" + extension
            })

        else:
            os.remove(archive)


    return data

def rename_identifyClient_darf():
    archives = []
    data = []

    for root, dirs, files in os.walk(extract_to_darf):
        for filename in files:
            basename, extension = os.path.splitext(filename)
            archives.append(extract_to_darf + "/" + basename + "" + extension)

    for archive in archives:
        pdf_file_obj = fitz.Document(archive)
        pdf_reader = pdf_file_obj.loadPage(0)
        pdf_text = str(pdf_reader.getText("text"))

        nfe = pdf_text.split('NF/Emitido:')[1].split('\n')[5].split(' ')[8]
        processDate = ''
        clientCode = ''
        clientNameAdjust = pdf_text.split('NF/Emitido:')[1].split('\n')[2].replace('&', 'E').replace('.', '').split(' ')
        if clientNameAdjust[1] == "da" or clientNameAdjust[1] == "DA" or clientNameAdjust[1] == "de" or clientNameAdjust[1] == "DE" or clientNameAdjust[1] == "E" or clientNameAdjust[1] == "e" or clientNameAdjust[1] == "do" or clientNameAdjust[1] == "DO":
            clientNameAdjust.remove(clientNameAdjust[1])
        clientName = clientNameAdjust[0] + " " + clientNameAdjust[1]
        clientCnpj = pdf_text.split('NF/Emitido:')[1].split('\n')[4].replace('.', '').replace('/', '').replace('-', '')
        metaName = pdf_text.split('Valores expressos em reais.\n')[1].split("\n")[0].replace('&', 'E').replace('.', '')
        metaCnpj = pdf_text.split('NF/Emitido:')[1].split('\n')[10].replace('.', '').replace('/', '').replace('-', '')

        os.rename(archive, extract_to_darf + "/" + clientName + " - NF " + nfe + " - (DARF)" + extension)

        data.append({
            "nfe": nfe,
            "processDate": processDate,
            "clientCnpj": clientCnpj,
            "clientCode": clientCode,
            "clientName": clientName,
            "metaCnpj": metaCnpj,
            "metaName": metaName,
            "type": "DARF",
            "archive": extract_to_darf + "/" + clientName + " - NF " + nfe + " - (DARF)" + extension
        })


    return data