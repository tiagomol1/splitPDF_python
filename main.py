import os
import time
from adjustFiles import split_pdf_pages
from adjustFiles import rename_identifyClient_boletos
from adjustFiles import rename_identifyClient_nfe
from adjustFiles import rename_identifyClient_darf
from adjustFiles import rename_identifyClient_informes
from fileOrganizer import organizer 

print('Iniciando Robô...')

data = []
boletoData = []
nfeData = []
darfData = []

os.mkdir('R:/FINANCEIRO/_automacao/boletos')
os.mkdir('R:/FINANCEIRO/_automacao/darf')
os.mkdir('R:/FINANCEIRO/_automacao/nfe')
# use the two functions
split_pdf_pages()
nfeData += rename_identifyClient_nfe()
boletoData += rename_identifyClient_boletos()
darfData += rename_identifyClient_darf()
rename_identifyClient_informes()

data = boletoData + nfeData + darfData 

organizer(data)

print("\n\nProcesso encerrando em:")
x = 5
while(x > 0):
    time.sleep(1)
    print(str(x))
    x = x - 1

os.rmdir('R:/FINANCEIRO/_automacao/boletos')
os.rmdir('R:/FINANCEIRO/_automacao/nfe')
os.rmdir('R:/FINANCEIRO/_automacao/darf')

print(r"Processo 100% concluido!")
time.sleep(3)