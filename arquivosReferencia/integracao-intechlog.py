import psycopg2
from json2xml import json2xml
import json 
from pprint import pprint


host = "144.22.196.58"
database = "lebes"
port = "5432"
user = "user_latromi"
password = "706h48qjLKyb"


connection = psycopg2.connect(host=host, database=database, port=port, user=user, password=password)
cursor = connection.cursor()



query = """
select jsonenvio

from manutencao.integracaointechlog_veiculo


where id = 12

"""

cursor.execute(query)
result = cursor.fetchall()


xml_list = []  

for row in result:
    json_content = row[0]

    #pprint(json_content) 
    #exit()
    
   # json_data = json.loads(json_content)  

    json_data={
    "programacaoEmbarque": {
        "chaveDocumentos": "1-1-1-56721",
        "numeroPedidoColeta": "10818",
        "seriePedidoColeta": "1",
        "chaveDocumentosColeta": "1-1-1-2-1-1-10818",
        "numeroProgramacaoEmbarque": "56721",
        "diferenciadorProgramacaoEmbarque": "1",
        "cpfMotorista": "015.264.200-58",
        "placaVeiculo": "IKJ3D28",
        "cnpjTransportadora": "27.913.322/0001-88",
        "locaisEntrega": [
            {
                "destinatarioCnpj": "96.662.168/0169-92",
                "dataInicioEntrega": "2023-08-29",
                "horaInicioEntrega": "07:00",
                "dataFimEntrega": "2023-08-29",
                "horaFimEntrega": "11:00",
                "quantida": "828,00",
                "peso": "24925,50",
                "cnpjRemetente": "72.144.066",
                "ctes": [
                    {
                        "descricaoCte": "CT-e 365645",
                        "chaveCte": "43230826524604000120570010003656451063656450"
                    }
                ]
            }
        ]
    }
}

    #pprint(json_data) 
    #exit()

    xml_content = json2xml.Json2xml(json_data).to_xml()
    xml_list.append(xml_content)

for xml_content in xml_list:
    print(xml_content)


cursor.close()
connection.close()