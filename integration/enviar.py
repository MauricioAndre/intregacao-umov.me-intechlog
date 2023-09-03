import http.client
conn = http.client.HTTPSConnection("api.umov.me")
headersList = {

 "Accept": "*/*",

 "Content-Type": "application/x-www-form-urlencoded"

}

def enviar(payload,uri):

    conn.request("POST", uri, payload, headersList)

    response = conn.getresponse()

    result = response.read()

    return result
