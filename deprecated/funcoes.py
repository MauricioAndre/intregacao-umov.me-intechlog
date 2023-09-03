###função deprecada
def trabalho(uriin, tipoxmlin, resultado):
    print(len(resultado) > 48)
    if len(resultado) > 48:
        limite=48
    else:
        limite=len(resultado)
        
    saida=[]
    print(len(resultado))
    print(limite)
    for i in range(limite):
     #   print(saida)    
        saida.append(resultado[0])
        resultado.pop(0)
    payload=templateselector.geraxml(saida,tipoxmlin)
  #  print(payload)
    result=enviar.enviar(payload,uriin)
    salvalog(str(result))
   # print(f'{len(resultado)}')
    if len(resultado) >0:
        trabalho(uriin, tipoxmlin, resultado)
###função deprecada