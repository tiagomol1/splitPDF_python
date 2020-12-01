import os

directory = r"/home/tiagomurilo/Documentos/pdfFinanceiro/diretorioFinal"
def organizer(archivesData):
    index = 0
    for archive in archivesData:
        index = index + 1
        if archive["processDate"] == '':
            for archiveCompare in archivesData:
                if archiveCompare["type"] == "NFe":
                    if archiveCompare["nfe"] == archive['nfe']:
                        os.rename(archive["archive"], directory + "/" + archiveCompare["processDate"] + "/" + archive["metaName"] + "/" + archive["clientName"] + " - NF " + archive["nfe"] + " - (" + archive["type"] + ")" + str(index) + ".pdf")
        else:
            if os.path.exists(directory + "/" + archive["processDate"]) == False:
                os.mkdir(directory + "/" + archive["processDate"])
            if os.path.exists(directory + "/" + archive["processDate"] + "/" + archive["metaName"]) == False:
                os.mkdir(directory + "/" + archive["processDate"] + "/" + archive["metaName"])

            os.rename(archive["archive"], directory + "/" + archive["processDate"] + "/" + archive["metaName"] + "/" + archive["clientName"] + " - NF " + archive["nfe"] + " - (" + archive["type"] + ")" + str(index) + ".pdf")