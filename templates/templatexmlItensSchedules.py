

def geraxmlbase(schedule,item):
    template=f"""
<scheduleItem>
    <schedule>
      <alternativeIdentifier>{schedule}</alternativeIdentifier>
    </schedule>
    <item>
      <alternativeIdentifier>{item}</alternativeIdentifier>
    </item>
  </scheduleItem>

"""
    return template

#print(geraxmlbase(1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1))

def geraxmlretorno(r):
 complemento=""
 complemento+=geraxmlbase(r[2],r[1])

 saida= f"""data=<scheduleItems>{complemento}</scheduleItems>"""
 #print(saida)
 return saida



