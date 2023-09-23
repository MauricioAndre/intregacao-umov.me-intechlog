from datetime import datetime
import re
xml='<result>\n  <resourceName>schedules</resourceName>\n  <size>1</size>\n  <entries>\n    <entry id="452710073" alternativeIdentifier="1-1-1-57437-96.662.168/0406-05-96.662.168" link="/schedule/452710073.xml"/>\n  </entries>\n</result>'
xml='<result>\n  <resourceName>scheduleItems</resourceName>\n  <size>1</size>\n  <entries>\n    <entry id="1329224606" link="/scheduleItem/1329224606.xml"/>\n  </entries>\n</result>'
xml='<result>\n  <resourceName>items</resourceName>\n  <size>1</size>\n  <entries>\n    <entry id="127604139" alternativeIdentifier="43230926524604000120570010003703841063703845" link="/item/127604139.xml"/>\n  </entries>\n</result>'

#xml='<result>\n  <statusCode>400</statusCode>\n  <errors>scheduleItems - 43230926524604000120570010003717981063717988: error.value.ScheuleOrItem.invalid;</errors>\n  <resourceName>scheduleItems</resourceName>\n</result>'

if 'error' in xml:
  xml = re.sub('<[^<]+>', "",xml)
  print(xml.split('\n'))
 # SELECT resourcename, size, entries, statuscode, errors, dtinc, entryid FROM intechlog.dados_umovme_log;
  descarte1,statuscode,entries,resourcename,descarte2 =xml.split('\n')
  entryid,errors=entries.split(':')
  entryid=entryid.split('-')
  entryid=''.join(entryid[1:2])
  size='1'
  print(entryid)
  now = datetime.now()
  dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

  query=f"INSERT INTO intechlog.dados_umovme_log(resourcename, size, entries, statuscode, errors, dtinc, entryid)VALUES ('{resourcename.replace(' ','')}', '{size.replace(' ','')}', '{entries.replace(' ','')}', '{statuscode.replace(' ','')}', '{errors.replace(' ','').replace(';','')}', '{dt_string}', '{entryid.replace(' ','')}')";
  print(query)
  ########################fazer insert
elif '<resourceName>scheduleItems</resourceName>' in xml:
  print('sa')
  ########################criar regra
else:
  descarte1,resourcename,size,descarte2,entries=xml.split('\n')[0:5]
  resourcename=re.sub('<[^<]+>', "",resourcename)
  size=re.sub('<[^<]+>', "",size)
  entries=re.sub('<[^<]+>', "",entries)
  print(descarte1,resourcename,size,descarte2,entries)
  statuscode='200'
  errors=''
  entryid=entries.split(' ')[5:6]
  entryid=' '.join(entryid).replace('\"','')
  entryid=' '.join(entryid.split('=')[1:2])
  print(entryid) 
  now = datetime.now()
  dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

  query=f"INSERT INTO intechlog.dados_umovme_log(resourcename, size, entries, statuscode, errors, dtinc, entryid)VALUES ('{resourcename.replace(' ','')}', '{size.replace(' ','')}', '{entries.replace(' ','')}', '{statuscode.replace(' ','')}', '{errors}', '{dt_string}', '{entryid.replace(' ','')}')";
  print(query)
 
 # print(xml.split('\n'))