import xml.etree.ElementTree as ET

#ACA DEFINIREMOS LAS FUNCIONES PARA MANEJAR ARCHIVOS XML

def create_XML_Request(*args):
    root = ET.Element('methodCall')
    ET.SubElement(root, 'methodName', args[0])
    parameters = ET.SubElement(root, 'params')
    for i in range(1, len(args)-1):
        param = ET.SubElement(parameters, 'param')
        value = ET.SubElement(param, 'value')
        ET.SubElement(value, to_xmlvalue(args[i]), args[i])
    return '<?xml version="1.0"?>\n' + ET.tostring(root, encoding='utf-8').decode('utf-8')

#<?xml version="1.0"?>
#<methodCall>
#    <methodName>examples.getStateName</methodName>
#    <params>
#        <param>
#            <value>
#               <i4>41</i4>
#            </value>
#        </param>
#    </params>
#</methodCall>


def to_xmlvalue(value):
    match type(value):
        case 'int':
            return 'int'
        case 'bool':
            return 'bool'
        case 'string':
            return 'string'
        case 'float':
            return 'float'
        case 'datetime.datetime':
            return 'dateTime.iso8601'
        # falta base64
        # falta struct
        # falta array
        