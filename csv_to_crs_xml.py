import csv
import xml.etree.ElementTree as ET
from datetime import datetime

def crear_crs_xml(csv_path, xml_path):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        # Raíz del documento
        root = ET.Element('CRS_OECD', version="2.0")
        for row in reader:
            # MessageSpec
            messagespec = ET.SubElement(root, 'MessageSpec')
            ET.SubElement(messagespec, 'SendingCompanyIN').text = row['SendingCompanyIN']
            ET.SubElement(messagespec, 'TransmittingCountry').text = row['TransmittingCountry']
            ET.SubElement(messagespec, 'ReceivingCountry').text = row['ReceivingCountry']
            ET.SubElement(messagespec, 'MessageType').text = row['MessageType']
            ET.SubElement(messagespec, 'MessageRefId').text = row['MessageRefId']
            ET.SubElement(messagespec, 'MessageTypeIndic').text = row['MessageTypeIndic']
            ET.SubElement(messagespec, 'ReportingPeriod').text = row['ReportingPeriod']
            ET.SubElement(messagespec, 'Timestamp').text = row['Timestamp']

            # CrsBody
            crsbody = ET.SubElement(root, 'CrsBody')
            # ReportingFI
            reportingfi = ET.SubElement(crsbody, 'ReportingFI')
            docspec = ET.SubElement(reportingfi, 'DocSpec')
            ET.SubElement(docspec, 'DocTypeIndic').text = "OECD1"  # Valor ejemplo
            ET.SubElement(docspec, 'DocRefId').text = row['MessageRefId'] + "-FI"
            ET.SubElement(docspec, 'CorrDocRefId')
            ET.SubElement(reportingfi, 'ResCountryCode').text = row['ReportingFI_ResCountryCode']
            in_elem = ET.SubElement(reportingfi, 'IN')
            in_elem.text = row['ReportingFI_IN']
            name_elem = ET.SubElement(reportingfi, 'Name')
            name_elem.text = row['ReportingFI_Name']
            address_elem = ET.SubElement(reportingfi, 'Address')
            address_elem.text = row['ReportingFI_Address']

            # ReportingGroup
            reportinggroup = ET.SubElement(crsbody, 'ReportingGroup')
            # AccountReport
            accountreport = ET.SubElement(reportinggroup, 'AccountReport')
            docspec2 = ET.SubElement(accountreport, 'DocSpec')
            ET.SubElement(docspec2, 'DocTypeIndic').text = "OECD1"
            ET.SubElement(docspec2, 'DocRefId').text = row['MessageRefId'] + "-AR"
            ET.SubElement(docspec2, 'CorrDocRefId')
            ET.SubElement(accountreport, 'AccountNumber').text = row['AccountNumber']
            ET.SubElement(accountreport, 'OpeningDate').text = row['OpeningDate']

            # AccountHolder
            accountholder = ET.SubElement(accountreport, 'AccountHolder')
            individual = ET.SubElement(accountholder, 'Individual')
            ET.SubElement(individual, 'ResCountryCode').text = row['AccountHolder_ResCountryCode']
            if row['AccountHolder_TIN']:
                tin_elem = ET.SubElement(individual, 'TIN')
                tin_elem.text = row['AccountHolder_TIN']
            name_person = ET.SubElement(individual, 'Name')
            ET.SubElement(name_person, 'FirstName').text = row['AccountHolder_FirstName']
            ET.SubElement(name_person, 'LastName').text = row['AccountHolder_LastName']
            address_person = ET.SubElement(individual, 'Address')
            address_person.text = row['AccountHolder_Address']
            if row['AccountHolder_Nationality']:
                ET.SubElement(individual, 'Nationality').text = row['AccountHolder_Nationality']
            if row['AccountHolder_BirthDate']:
                birthinfo = ET.SubElement(individual, 'BirthInfo')
                ET.SubElement(birthinfo, 'BirthDate').text = row['AccountHolder_BirthDate']

            ET.SubElement(accountreport, 'AccountBalance').text = row['AccountBalance']

            # Payment (opcional)
            if row['Payment_Type'] and row['Payment_Amount']:
                payment = ET.SubElement(accountreport, 'Payment')
                ET.SubElement(payment, 'Type').text = row['Payment_Type']
                ET.SubElement(payment, 'PaymentAmnt').text = row['Payment_Amount']

        # Guardar XML
        tree = ET.ElementTree(root)
        tree.write(xml_path, encoding='utf-8', xml_declaration=True)

if __name__ == "__main__":
    crear_crs_xml("plantilla_crs.csv", "salida_crs.xml")