import integration.enviar as enviar
import conexoes.conectava as conectava
import templates.templateselector as templateselector
import integration.geralog as geralog
def processa(queryin,uriin,tipoxmlin):
    resultado=conectava.conecta(queryin)
   # print(resultado)
    for r in resultado:
        payload=templateselector.geraxml(r,tipoxmlin)
        print(payload)
        result=enviar.enviar(payload,uriin)
        print(result)
        geralog.salvalog(str(result))