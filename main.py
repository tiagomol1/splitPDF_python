import os
import time
from adjustFiles import split_pdf_pages
from adjustFiles import rename_identifyClient_boletos
from adjustFiles import rename_identifyClient_nfe
from adjustFiles import rename_identifyClient_darf
from fileOrganizer import organizer 

data = []
boletoData = []
nfeData = []
darfData = []

os.mkdir('/home/tiagomurilo/Documentos/pdfFinanceiro/boletos')
os.mkdir('/home/tiagomurilo/Documentos/pdfFinanceiro/darf')
os.mkdir('/home/tiagomurilo/Documentos/pdfFinanceiro/nfe')
# use the two functions
split_pdf_pages()
boletoData += rename_identifyClient_boletos()
nfeData += rename_identifyClient_nfe()
darfData += rename_identifyClient_darf()

data = boletoData + nfeData + darfData

organizer(data)

print("Processo encerrando em:")
x = 15
while(x > 0):
    time.sleep(1)
    print(str(x))
    x = x - 1

print("Finalizado!")
os.rmdir('/home/tiagomurilo/Documentos/pdfFinanceiro/boletos')
os.rmdir('/home/tiagomurilo/Documentos/pdfFinanceiro/darf')
os.rmdir('/home/tiagomurilo/Documentos/pdfFinanceiro/nfe')
