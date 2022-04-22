# modulos importados
import PyPDF2
import os
import fitz
import time

# variaveis
original_files = r"R:/FINANCEIRO/_automacao/original"
extract_to_boletos = r"R:/FINANCEIRO/_automacao/boletos"
extract_to_darf = r"R:/FINANCEIRO/_automacao/darf"
extract_to_nfe = r"R:/FINANCEIRO/_automacao/nfe"
extract_to_informes = r"R:/FINANCEIRO/_automacao/ajustados/informes"

def split_pdf_pages():
    # pegando diretório e arquivos
    print('- Separando paginas...')
    for root, dirs, files in os.walk(original_files):
        # para cada arquivo se busca o nome e extenção
        for filename in files:
            directory = r"R:/FINANCEIRO/_automacao/ajustados"
            basename, extension = os.path.splitext(filename)
            # verifica se arquivo é PDF
            if extension == ".pdf":
                # referencia a pasta com o nome do novo arquivo
                fullpath = root + "/" + basename + extension
                pdf_file_obj = fitz.Document(fullpath)
                pdf_reader = pdf_file_obj.loadPage(0)
                pdf_text = str(pdf_reader.getText("text"))
                pdf_file_obj.close()

                if pdf_text.find("BRADESCO") != -1:
                    directory = extract_to_boletos
                elif pdf_text.find("Impressão NF-e") != -1 or pdf_text.find("PREFEITURA MUNICIPAL DE JOINVILLE") != -1:
                    directory = extract_to_nfe
                elif pdf_text.find("Itaú Unibanco") != -1:
                    directory = extract_to_boletos
                elif pdf_text.find("BANRISUL") != -1:
                    directory = extract_to_boletos
                elif pdf_text.find("PIS / COFINS / CSLL") != -1:
                    directory = extract_to_darf
                elif pdf_text.find("Documento de Arrecadação de Receitas Federais") != -1:
                    directory = extract_to_darf
                elif pdf_text.find("MUNICÍPIO DE JARAGUÁ DO SUL") != -1:
                    directory = extract_to_nfe
                elif pdf_text.find("Comprovante de Impostos Retidos") != -1:
                    if os.path.exists(extract_to_informes) == False:
                        os.mkdir(extract_to_informes)
                    directory = extract_to_informes
                elif pdf_text == "":
                    directory = r"R:/FINANCEIRO/_automacao/arquivos incorretos"

                # abre o pdf no modo leitura
                opened_pdf = PyPDF2.PdfFileReader(open(fullpath, "rb"))
              
                # conta paginas achadas no pdf
                for i in range(opened_pdf.getNumPages()):
                    # write the page to a new pdf
                    output = PyPDF2.PdfFileWriter()
                    output.addPage(opened_pdf.getPage(i))

                    with open(directory + "/" + basename + " - " + str(i) + ".pdf", "wb") as output_pdf:
                        output.write(output_pdf)
    print('- Separação de paginas finalizada.')

def rename_identifyClient_boletos():
    archives = []
    data = []

    print('\n- Separando BOLETOS...')
    for root, dirs, files in os.walk(extract_to_boletos):
        for filename in files:
            basename, extension = os.path.splitext(filename)

            archives.append(extract_to_boletos + "/" + basename + "" + extension)

    for archive in archives:
        pdf_file_obj = fitz.Document(archive)
        pdf_reader = pdf_file_obj.loadPage(0)
        pdf_text = str(pdf_reader.getText("text"))
        pdf_file_obj.close()

        if pdf_text.find("BRADESCO") != -1:
            nfe = pdf_text.split('APÓS 10 DIAS VENCIDO SUJEITO A ENVIO A CARTÓRIO')[3].split('\n')[5].split('\n')[0].replace('/', ' ')
            clientData = pdf_text.split("Pagador")[3].split("\n")[12].replace('-', '')
            clientCnpj = clientData.split('  ')[0].replace('.', '').replace('/', '')
            clientCode = clientData.split('  ')[1]
            clientName = ''
            clientName = clientData.replace('&', 'E').split('  ')[2].replace('-', '').replace('&', '').replace('.', '').replace('/', '')
            metaNameAdjust = pdf_text.split("Pagador")[3].split("\n")[2].replace('-', '').split(' ')
            if(metaNameAdjust[1] == "da" or metaNameAdjust[1] == "DA" or metaNameAdjust[1] == "de" or metaNameAdjust[1] == "DE" or metaNameAdjust[1] == "E" or metaNameAdjust[1] == "e"):
                metaNameAdjust.remove(metaNameAdjust[1])
            metaName = metaNameAdjust[0] + " " + metaNameAdjust[1]
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
            clientName = pdf_text.split("Pagador\n")[1].split("\n")[0].replace('.', '').replace('&', 'E').replace('/','')       
            clientCnpj = pdf_text.split("Beneficiário")[2].split("\n")[1].replace('.', '').replace('/', '').replace('-', '')
            clientCode = '-'
            metaNameAdjust = pdf_text.split("APÓS 10 DIAS VENCIDO SUJEITO A ENVIO A CARTÓRIO")[1].split("\n")[1].split("-")[0].strip().split(' ')
            if(metaNameAdjust[1] == "da" or metaNameAdjust[1] == "DA" or metaNameAdjust[1] == "de" or metaNameAdjust[1] == "DE" or metaNameAdjust[1] == "E" or metaNameAdjust[1] == "e"):
                metaNameAdjust.remove(metaNameAdjust[1])
            metaName = metaNameAdjust[0] + " " + metaNameAdjust[1]
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
            clientName = pdf_text.split('Pagador\n')[1].split('\n')[0].replace('-', '').replace('&', '').replace('.', '').replace('/', '')
            clientCnpj = pdf_text.split('Pagador\n')[1].split('\n')[2].replace('.', '').replace('/', '').replace('-', '')
            clientCode = '-'
            metaCnpj = pdf_text.split('CPF/CNPJ\n ')[1].split('\n')[0].replace('.', '').replace('/', '').replace('-', '')
            metaNameAdjust = pdf_text.split('CPF/CNPJ - \n')[2].split('\n')[3].split(" - ")[0].split(' ')
            if(metaNameAdjust[1] == "da" or metaNameAdjust[1] == "DA" or metaNameAdjust[1] == "de" or metaNameAdjust[1] == "DE" or metaNameAdjust[1] == "E" or metaNameAdjust[1] == "e"):
                metaNameAdjust.remove(metaNameAdjust[1])
            metaName = metaNameAdjust[0] + " " + metaNameAdjust[1]

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

    print('- Separacao de BOLETOS concluido.')
    return data

def rename_identifyClient_nfe():
    archives = []
    compareArchive = []
    data = []

    print("\n- Separando NFe...") 

    for root, dirs, files in os.walk(extract_to_nfe):
        for filename in files:
            basename, extension = os.path.splitext(filename)
            archives.append(extract_to_nfe + "/" + basename + "" + extension)
    for archive in archives:

        try:
            pdf_file_obj = fitz.Document(archive)
            pdf_reader = pdf_file_obj.loadPage(0)
            pdf_text = str(pdf_reader.getText("text"))
            
            pdf_file_obj.close()

            if pdf_text.find("Numero da NF-em ") != -1 or pdf_text.find("Número da NF-em ") != -1 :

                nfe = pdf_text.split("Número da NF-em ")[1].split(" ")[0].split("\n")[1]
                clientCode = pdf_text.split("TOMADOR DE SERVIÇO")[1].split("Nome/Razão Social:\n")[1].split("-")[0]
                clientName = pdf_text.split("TOMADOR DE SERVIÇO")[1].split("Nome/Razão Social:\n")[1].split("-")[1].split("\n")[0].replace('.', '').replace('&', 'E').replace('/', '')
                clientCnpj = pdf_text.split("TOMADOR DE SERVIÇO")[1].split("CPF/CNPJ:\n")[1].split('\n')[0].replace(".", "").replace('-', '').replace('/', '')
                metaCnpj = pdf_text.split("PRESTADOR DE SERVIÇOS")[1].split("CPF/CNPJ:\n")[1].split('\n')[0].replace(".", "").replace('-', '').replace('/', '')
                metaNameAdjust = pdf_text.split("PRESTADOR DE SERVIÇOS")[1].split("Razão Social:\n")[1].split('\n')[0].replace('.', '').replace('&', 'E').split(' ')
                if(metaNameAdjust[1] == "da" or metaNameAdjust[1] == "DA" or metaNameAdjust[1] == "de" or metaNameAdjust[1] == "DE" or metaNameAdjust[1] == "E" or metaNameAdjust[1] == "e"):
                    metaNameAdjust.remove(metaNameAdjust[1])
                metaName = metaNameAdjust[0] + " " + metaNameAdjust[1]
                clientNameAdjust = clientName.split(' ')
                if(clientNameAdjust[1] == "da" or clientNameAdjust[1] == "DA" or clientNameAdjust[1] == "de" or clientNameAdjust[1] == "DE" or clientNameAdjust[1] == "E" or clientNameAdjust[1] == "e" or clientNameAdjust[1] == "RESIDENCIAL" or clientNameAdjust[1] == "CONDOMÍNIO" or clientNameAdjust[1] == "Residencial" or clientNameAdjust[1] == "Condomínio" or clientNameAdjust[1] == "CONDOMINIO" or clientNameAdjust[1] == "Condominio"):
                    clientNameAdjust.remove(clientNameAdjust[1])
                clientName = clientNameAdjust[0] + " " + clientNameAdjust[1]
                processDate = pdf_text.split('Data e Hora de Emissão')[1].split(' ')[1].split('\n')[1].replace('/', '-')[3:10]

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

            elif pdf_text.find("MUNICÍPIO DE JARAGUÁ DO SUL") != -1 or pdf_text.find("Município: Jaraguá do Sul") != -1:
                
                nfe = pdf_text.split("Data da emissão da nota")[0].split('\n')[6]
                clientCode = ""
                clientName = pdf_text.split("SECRETARIA MUNICIPAL DA FAZENDA")[1].split('\n')[1].replace('.', '').replace('&', 'E').replace('/', '').replace('.', '')
                clientCnpj = pdf_text.split("Telefone:")[1].split('\n')[1]
                processDate = pdf_text.split('\n')[2].split(' ')[0].replace('/', '-')[3:10]
                
                if pdf_text.find("Página 1/1") > -1:
                    os.rename(archive, extract_to_nfe + "/" + clientName + " - NF " + nfe + " - (NFe )" + extension)
                    data.append({
                        "nfe": nfe,
                        "processDate": processDate,
                        "clientCnpj": clientCnpj,
                        "clientCode": clientCode,
                        "clientName": clientName,
                        "metaCnpj": "24336426000189",
                        "metaName": "JARAGUA GESTAO",
                        "type": "NFe",
                        "archive": extract_to_nfe + "/" + clientName + " - NF " + nfe + " - (NFe )" + extension
                    })
                    break
        finally:
            continue

    archives = []
    for root, dirs, files in os.walk(extract_to_nfe):
        for filename in files:
            basename, extension = os.path.splitext(filename)
            archives.append(extract_to_nfe + "/" + basename + "" + extension)
    x = 0
    for archive in archives:

        try:
            pdf_file_obj = fitz.Document(archive)
            pdf_reader = pdf_file_obj.loadPage(0)
            pdf_text = str(pdf_reader.getText("text"))
            
            pdf_file_obj.close()

            if pdf_text.find("MUNICÍPIO DE JARAGUÁ DO SUL") != -1 or pdf_text.find("Município: Jaraguá do Sul") != -1:              
                if pdf_text.find("Página 1/2") > -1:

                    nfe = pdf_text.split("Data da emissão da nota")[0].split('\n')[6]
                    clientCode = ""
                    clientName = pdf_text.split("SECRETARIA MUNICIPAL DA FAZENDA")[1].split('\n')[1].replace('.', '').replace('&', 'E').replace('/', '').replace('.', '')
                    clientCnpj = pdf_text.split("Telefone:")[1].split('\n')[1]
                    processDate = pdf_text.split('\n')[2].split(' ')[0].replace('/', '-')[3:10]

                    for archive2 in archives:
                        if pdf_text.find("Página 1/2") > -1:
                            pdf_file_obj2 = fitz.Document(archive2)
                            pdf_reader2 = pdf_file_obj2.loadPage(0)
                            pdf_text2 = str(pdf_reader2.getText("text"))
                            pdf_file_obj2.close()
                            nfeToCompare = pdf_text2.split("Data da emissão da nota")[0].split('\n')[6]
                            if pdf_text2.find("Página 2/2") == -1:
                                if nfeToCompare == nfe:

                                    merger = PyPDF2.PdfFileMerger()
                                    merger.append(archive)
                                    merger.append(archive2)
                                    time.sleep(1)
                                    x = x + 1
                                    merger.write('R:/FINANCEIRO/_automacao/nfe/teste'+ str(x) +'.pdf')
                                    merger.close()
                                    os.rename('R:/FINANCEIRO/_automacao/nfe/teste'+ str(x) +'.pdf', extract_to_nfe + "/" + clientName + " - NF " + nfe + " - (NFe )" + extension)
                                    data.append({
                                        "nfe": nfe,
                                        "processDate": processDate,
                                        "clientCnpj": clientCnpj,
                                        "clientCode": clientCode,
                                        "clientName": clientName,
                                        "metaCnpj": "24336426000189",
                                        "metaName": "JARAGUA GESTAO",
                                        "type": "NFe",
                                        "archive": extract_to_nfe + "/" + clientName + " - NF " + nfe + " - (NFe )" + extension
                                    })
    
        finally:
            continue

    print("- Separacao de NFe concluido.") 
    return data

def rename_identifyClient_darf():

    archives = []
    data = []

    print('\n- Separando DARF...')
    for root, dirs, files in os.walk(extract_to_darf):
        for filename in files:
            basename, extension = os.path.splitext(filename)
            archives.append(extract_to_darf + "/" + basename + "" + extension)


    index = 0
    for archive in archives:
        
        pdf_file_obj = fitz.Document(archive)
        pdf_reader = pdf_file_obj.loadPage(0)
        pdf_text = str(pdf_reader.getText("text"))
        pdf_file_obj.close()

        if pdf_text.find("PIS / COFINS / CSLL") != -1:

            index = index + 1

            nfe = pdf_text.split('NF/Emitido:')[1].split('\n')[5].strip().replace('.', '')
            if pdf_text.split('NF/Emitido:')[1].split('\n')[5].find(',') > -1:
                nfe = pdf_text.split('NF/Emitido:')[1].split('\n')[4].strip().replace('.', '')
            processDate = ""
            clientCode = ""
            clientName = pdf_text.split('NF/Emitido:')[1].split('\n')[2].replace('&', 'E').replace('.', '').replace('/', '')
            clientCnpj = pdf_text.split('NF/Emitido:')[1].split('\n')[4].replace('.', '').replace('/', '').replace('-', '')
            metaNameAdjust = pdf_text.split('Valores expressos em reais.\n')[1].split("\n")[0].replace('&', 'E').replace('.', '').split(' ')
            if(metaNameAdjust[1] == "da" or metaNameAdjust[1] == "DA" or metaNameAdjust[1] == "de" or metaNameAdjust[1] == "DE" or metaNameAdjust[1] == "E" or metaNameAdjust[1] == "e"):
                metaNameAdjust.remove(metaNameAdjust[1])
            metaName = metaNameAdjust[0] + " " + metaNameAdjust[1]
            metaCnpj = pdf_text.split('NF/Emitido:')[1].split('\n')[10].replace('.', '').replace('/', '').replace('-', '')

            os.rename(archive, extract_to_darf + "/" + clientName + " - NF " + nfe + " - (DARF 5952)" + str(index)  + extension)

            data.append({
                "nfe": nfe,
                "processDate": processDate,
                "clientCnpj": clientCnpj,
                "clientCode": clientCode,
                "clientName": clientName,
                "metaCnpj": metaCnpj,
                "metaName": metaName,
                "type": "DARF 5952",
                "archive": extract_to_darf + "/" + clientName + " - NF " + nfe + " - (DARF 5952)" + str(index)  + extension
            })
        else:

            index = index + 1

            nfe = pdf_text.split('NF/Emitido:')[1].split('\n')[4].strip().replace('.', '')
            if pdf_text.split('NF/Emitido:')[1].split('\n')[4].find(',') > -1:
                nfe = pdf_text.split('NF/Emitido:')[1].split('\n')[4].strip().replace('.', '')
            processDate = ""
            clientCode = ""
            clientNameAdjust = pdf_text.split('NF/Emitido:')[1].split('\n')[5].replace('&', 'E').replace('.', '').replace('/', '').split(' ')
            if(clientNameAdjust[1] == "da" or clientNameAdjust[1] == "DA" or clientNameAdjust[1] == "de" or clientNameAdjust[1] == "DE" or clientNameAdjust[1] == "E" or clientNameAdjust[1] == "e" or clientNameAdjust[1] == "RESIDENCIAL" or clientNameAdjust[1] == "CONDOMÍNIO" or clientNameAdjust[1] == "Residencial" or clientNameAdjust[1] == "Condomínio" or clientNameAdjust[1] == "CONDOMINIO" or clientNameAdjust[1] == "Condominio"):
                clientNameAdjust.remove(clientNameAdjust[1])
            clientName = clientNameAdjust[0] + " " + clientNameAdjust[1]
            clientCnpj = pdf_text.split('NF/Emitido:')[1].split('\n')[7].replace('.', '').replace('/', '').replace('-', '')
            metaNameAdjust = pdf_text.split('Valores expressos em reais.\n')[1].split("\n")[5].replace('&', 'E').replace('.', '').split(' ')
            if(metaNameAdjust[1] == "da" or metaNameAdjust[1] == "DA" or metaNameAdjust[1] == "de" or metaNameAdjust[1] == "DE" or metaNameAdjust[1] == "E" or metaNameAdjust[1] == "e"):
                metaNameAdjust.remove(metaNameAdjust[1])
            metaName = metaNameAdjust[0] + " " + metaNameAdjust[1]
            metaCnpj = pdf_text.split('01 NOME / TELEFONE')[1].split('\n')[1].replace('/', '').replace('.', '').replace('-', '').replace(' ', '')

            os.rename(archive, extract_to_darf + "/" + clientName + " - NF " + nfe + " - (DARF 1708)" + str(index)  + extension)

            data.append({
                "nfe": nfe,
                "processDate": processDate,
                "clientCnpj": clientCnpj,
                "clientCode": clientCode,
                "clientName": clientName,
                "metaCnpj": metaCnpj,
                "metaName": metaName,
                "type": "DARF 1708",
                "archive": extract_to_darf + "/" + clientName + " - NF " + nfe + " - (DARF 1708)" + str(index) + extension
            })
    
    print('- Separacao de DARF concluida.')
    return data

def rename_identifyClient_informes():

    archives = []

    print('\n- Separando Informes...')
    for root, dirs, files in os.walk(extract_to_informes):
        for filename in files:
            basename, extension = os.path.splitext(filename)
            archives.append(extract_to_informes + "/" + basename + "" + extension)

    index = 0
    time.sleep(2)
    for archive in archives:
        pdf_file_obj = fitz.Document(archive)
        pdf_reader = pdf_file_obj.loadPage(0)
        pdf_text = str(pdf_reader.getText("text"))
        pdf_file_obj.close()

        index = index + 1

        clientName = pdf_text.split('\n')[8].replace('   ', '').replace('.', '').replace('/', '').replace('&','')
        os.rename(archive, extract_to_informes + "/" + clientName + " . " + str(index)  + extension)
    
    print('\n- Separação de Informes concluido.')
