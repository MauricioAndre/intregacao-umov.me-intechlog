

def geraxmlbase(description,alternativeIdentifier):
    template=f"""
<item>
  <subGroup>
    <alternativeIdentifier>notas_fiscais</alternativeIdentifier>
  </subGroup>
  <description>{description}</description>
  <active>true</active>
  <alternativeIdentifier>{alternativeIdentifier}</alternativeIdentifier>
</item>

"""
    return template

#print(geraxmlbase(1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1))

def geraxmlretorno(response):
 complemento=""
 for r in response:
    complemento+=geraxmlbase(r[0],r[1])

 saida= f"""data=<items>{complemento}</items>"""
 #print(saida)
 return saida



