

def geraxmlbase(scheduleType,serviceLocal,team,teamExecution,agent,alternativeIdentifier,date1,hour1,executionForecastEndDate,executionForecastEndTime,observation,situation,customField1,customField2,tar_veiculo,tar_embarcador,lista_ctes):
    template=f"""<schedule>
    <scheduleType>
        <alternativeIdentifier>{scheduleType}</alternativeIdentifier>
    </scheduleType>
    <serviceLocal>
        <alternativeIdentifier>{serviceLocal}</alternativeIdentifier>
    </serviceLocal>
    <active>true</active>
    <activitiesOrigin>7</activitiesOrigin>
    <sendNotification>true</sendNotification>
    <team>
        <alternativeIdentifier>{team}</alternativeIdentifier>
    </team>
    <teamExecution>{teamExecution}</teamExecution>
    <agent>
        <alternativeIdentifier>{agent}</alternativeIdentifier>
    </agent>
    <alternativeIdentifier>{alternativeIdentifier}</alternativeIdentifier>
    <date>{date1}</date>
    <hour>{hour1}</hour>
    <executionForecastEndDate>{executionForecastEndDate}</executionForecastEndDate>
    <executionForecastEndTime>{executionForecastEndTime}</executionForecastEndTime>
    <observation>{observation}</observation>
    <situation>
        <id>{situation}</id>
    </situation>
    <customField1>{customField1}</customField1>
    <customField2>{customField2}</customField2>
    <customFields>
        <tar_veiculo>
        <alternativeIdentifier>{tar_veiculo}</alternativeIdentifier>
        </tar_veiculo>
        <tar_embarcador>
        <alternativeIdentifier>{tar_embarcador}</alternativeIdentifier>
        </tar_embarcador>
        <lista_ctes>{lista_ctes}</lista_ctes>
    </customFields></schedule>"""
    return template

#print(geraxmlbase(1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1))

def geraxmlretorno(r):
 complemento=""
 #for r in response:
 complemento+=geraxmlbase(r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8],r[9],r[10],r[11],r[12],r[13],r[14],r[15],r[16])

 saida= f"""data=<schedules>{complemento}</schedules>"""
 #print(saida)
 return saida



