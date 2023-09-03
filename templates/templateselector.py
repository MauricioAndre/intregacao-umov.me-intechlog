import templates.templatexmlEntrega as entrega
import templates.templatexmlItens as items
import templates.templatexmlItensSchedules as scheduleitems

def geraxml(resultado,tipoxml):
    if tipoxml=='entregas':
       saida= entrega.geraxmlretorno(resultado)
    if tipoxml=='items':
        saida= items.geraxmlretorno(resultado)
    if tipoxml=='entregasitems':    
        saida= scheduleitems.geraxmlretorno(resultado)
    return saida

