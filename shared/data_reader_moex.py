import xml.etree.ElementTree as ET


class DataReaderMOEX():
    '''
    DataReaderMOEX class used for MOEX xml parsing
    '''

    def __init__(self, path_to_xml):
        self.file_path = path_to_xml

    def get_total_rows(self):
        '''
        Gets TOTAL attribute value from the row element
        '''
        tree = ET.parse(self.file_path)
        rows = tree.getroot().findall('./data/rows/row')
        total_rows = list(filter(lambda row: 'TOTAL' in row.attrib, rows))
        if total_rows:
            total_value = int(total_rows[0].get('TOTAL'))
            return total_value
        else:
            raise KeyError('Total attribute is not found in ' + self.file_path)
