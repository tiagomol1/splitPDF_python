import os

directory = r"C:/Users/Tiago Murilo/Desktop/diretorioFinal"
def organizer(archivesData):
    index = 0

    print('\n- Renomeando Arquivos e salvando no diretorio final.')
    for archive in archivesData:
        index = index + 1
        if archive["processDate"] == '':
            x = 0
            for archiveCompare in archivesData:
                if len(archivesData) - 1 == x:
                    os.rename(archive["archive"], "C:/Users/Tiago Murilo/Desktop/ajustados/" + archive["clientName"] + " - NF " + archive["nfe"] + " - (" + archive["type"] + ")" + str(index) + ".pdf")

                nfeToCompara = archiveCompare["nfe"]
                if archiveCompare["type"] == "Boleto":
                    nfeToCompara = archiveCompare["nfe"].split(" ")[0]

                if nfeToCompara == archive['nfe'] and archiveCompare['processDate'] != '':
                    os.rename(archive["archive"], directory + "/" + archiveCompare["processDate"] + "/" + archive["metaName"] + "/" + archive["clientName"] + " - NF " + archive["nfe"] + " - (" + archive["type"] + ")" + str(index) + ".pdf")
                    break
                x = x + 1

        else:
            if os.path.exists(directory + "/" + archive["processDate"]) == False:
                os.mkdir(directory + "/" + archive["processDate"])
            if os.path.exists(directory + "/" + archive["processDate"] + "/" + archive["metaName"]) == False:
                os.mkdir(directory + "/" + archive["processDate"] + "/" + archive["metaName"])

            os.rename(archive["archive"], directory + "/" + archive["processDate"] + "/" + archive["metaName"] + "/" + archive["clientName"] + " - NF " + archive["nfe"] + " - (" + archive["type"] + ")" + str(index) + ".pdf")