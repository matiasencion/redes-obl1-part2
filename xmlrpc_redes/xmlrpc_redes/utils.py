import xml.etree.ElementTree as ET
import datetime

#ACA DEFINIREMOS LAS FUNCIONES PARA MANEJAR ARCHIVOS XML

# RETORNA UN STRING CON EL XML-RPC
def create_XML_Request(*args):
    root = ET.Element('methodCall')
    ET.SubElement(root, 'methodName', args[0])
    parameters = ET.SubElement(root, 'params')
    for i in range(1, len(args)-1):
        param = ET.SubElement(parameters, 'param')
        value = ET.SubElement(param, 'value')
        ET.SubElement(value, to_xmlvalue(args[i]), str(args[i]))
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

# RETORNA UNA LISTA CON: nombre del metodo -> parametro1 -> parametro2 -> ...
def translate_XML_Request(xml_request): 
    root = ET.fromstring(xml_request)
    method = [] # es una lista
    method.append(root.find('methodName').text)
    parameters = root.findall('param')
    for p in parameters: # posiblemente se pueda recorrer directamente con los values
        value = p.find('value')
        type_and_value = list(value)[0]
        method.append(from_xmlvalue(type_and_value)) # agregamos los parametros (en su tipo correspontiente)
    return method

def to_xmlvalue(value):
    match type(value):
        case 'int':
            return 'int'
        case 'bool':
            return 'boolean'
        case 'string':
            return 'string'
        case 'float':
            return 'double'
        case 'datetime.datetime':
            return 'dateTime.iso8601'
        # falta base64
        # falta struct
        # falta array
        
def from_xmlvalue(value): # te los devuelve en su tipo correspondiente!
    match value.tag:
        case 'i4':
            return int(value.text)
        case 'int':
            return int(value.text)
        case 'boolean':
            return bool(value.text)
        case 'string':
            return str(value.text)
        case 'double':
            return float(value.text)
        case 'dateTime.iso8601':
            return datetime.fromisoformat(value.text) # lo transformamos a datetime
        # falta base64
        # falta struct
        # falta array