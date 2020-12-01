from adjustFiles import split_pdf_pages
from adjustFiles import rename_identifyClient_boletos
from adjustFiles import rename_identifyClient_nfe
from adjustFiles import rename_identifyClient_darf
from fileOrganizer import organizer 

data = []
boletoData = []
nfeData = []
darfData = []

# use the two functions
split_pdf_pages()
boletoData += rename_identifyClient_boletos()
nfeData += rename_identifyClient_nfe()
darfData += rename_identifyClient_darf()

data = boletoData + nfeData + darfData
print(data)

organizer(data)


