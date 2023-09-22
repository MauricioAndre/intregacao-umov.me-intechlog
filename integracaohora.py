import conexoes.queries as queries
import integration.processa as processa    
import os
import dotenv

dotenv.load_dotenv()
token=os.getenv("TOKEN")

tipoxml='entregas'
uri=f"/CenterWeb/api/{token}/batch/schedules.xml"
query=queries.entregashora
processa.processa(query,uri,tipoxml)


tipoxml='items'
query=queries.itemshora
uri=f"/CenterWeb/api/{token}/batch/items.xml"
print(processa.processa(query,uri,tipoxml))


tipoxml='entregasitems'
query=queries.itemshora
uri=f"/CenterWeb/api/{token}/batch/scheduleItems.xml"
print(processa.processa(query,uri,tipoxml))

