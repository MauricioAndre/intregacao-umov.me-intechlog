import conexoes.queries as queries
import integration.processa as processa    
import os
import dotenv

dotenv.load_dotenv()
token=os.getenv("TOKEN")

tipoxml='entregas'
uri=f"/CenterWeb/api/{token}/batch/schedules.xml"
query=queries.entregas
processa.processa(query,uri,tipoxml)


tipoxml='items'
query=queries.items
uri=f"/CenterWeb/api/{token}/batch/items.xml"
print(processa.processa(query,uri,tipoxml))


tipoxml='entregasitems'
query=queries.items
uri=f"/CenterWeb/api/{token}/batch/scheduleItems.xml"
print(processa.processa(query,uri,tipoxml))

