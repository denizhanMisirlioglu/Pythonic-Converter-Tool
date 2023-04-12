import sys
import pandas as pd 
import json
import xml.etree.ElementTree as ET
from lxml import etree
from pandas import DataFrame

#documentation :
 # My program does not work for csv other than DEPARTMENTS.csv
 # You have to use DEPARTMENTS.csv for csv_to_json and csv_to_xml operations.
 # XML_VALIDATE.xsd is for my xml validate operations.

 #  This is an example usage of my converter tool.

 #python3 2016510054.py DEPARTMENTS.csv csv_to_xml 1 
 #python3 2016510054.py csv_to_xml xml_to_csv 2
 #python3 2016510054.py csv_to_xml xml_to_json 3
 #python3 2016510054.py xml_to_json json_to_xml 4
 #python3 2016510054.py DEPARTMENTS.csv csv_to_json 5
 #python3 2016510054.py csv_to_json json_to_csv 6
 #python3 2016510054.py csv_to_xml XML_VALIDATE.xsd 7  must return # True 
 #python3 2016510054.py json_to_xml XML_VALIDATE.xsd 7 must return # True  

 #I shared some source links that i used in the code

input_name = (sys.argv[1])           #arguments for command line
output_name = (sys.argv[2])
conveting_type = int(sys.argv[3])

if (sys.argv[3] == '1'):  # csv to xml  read csv with pandas ,create pandas dataframe then  create xml with  dataframes
  df = pd.read_csv(sys.argv[1],delimiter=';')
  df.loc[df['OKUL_BİRİNCİSİ_KONTENJANI'].isna(),'OKUL_BİRİNCİSİ_KONTENJANI'] ='0' # convert NaN to 0 to prevent any errors at xsd validation
  df.loc[df['GEÇEN_YIL_MİN_SIRALAMA'].isna(),'GEÇEN_YIL_MİN_SIRALAMA'] ='0'
  df.loc[df['GEÇEN_YIL_MİN_PUAN'].isna(),'GEÇEN_YIL_MİN_PUAN'] ='0'

  df.loc[df['BURS'].isna(),'BURS'] ='0'
  df = df.fillna('') # converting NaN which is causes errors to ''  

  xml_doc = ET.Element('departments')    #building xml with my dataframe
  for index,row in df.iterrows():
    university = ET.SubElement(xml_doc,'university',uType=str(df.iloc[index,0]),name=str(df.iloc[index,1]))
    item = ET.SubElement(university,'item',faculty=str(df.iloc[index,2]),id=str(df.iloc[index,3]))
    name = ET.SubElement(item,'name',second=str(df.iloc[index,6]),lang=str(df.iloc[index,5])).text =str(df.iloc[index,4])
    period = ET.SubElement(item,'period').text=str(df.iloc[index,8])
    quota = ET.SubElement(item,'quota',spec=str(df.iloc[index,11])).text=str(df.iloc[index,10])
    field = ET.SubElement(item,'field').text=str(df.iloc[index,9])
    last_min_score = ET.SubElement(item,'last_min_score',order=str(df.iloc[index,12])).text=str(df.iloc[index,13])
    grant = ET.SubElement(item,'grant').text=str(df.iloc[index,7])

  def prettify(element, indent='  '):  # I took ' prettify' function  and some other codes for building xml  from this source :https://www.youtube.com/watch?v=QiTMhvI4WrQ

      queue = [(0, element)]  # (level, element)
      while queue:
          level, element = queue.pop(0)
          children = [(level + 1, child) for child in list(element)]
          if children:
              element.text = '\n' + indent * (level+1)  # for child open
          if queue:
              element.tail = '\n' + indent * queue[0][0]  # for sibling open
          else:
              element.tail = '\n' + indent * (level-1)  # for parent close
          queue[0:0] = children  # prepend so children come before siblings

  prettify(xml_doc)
  tree = ET.ElementTree(xml_doc)
  tree.write(sys.argv[2],encoding='UTF-8',xml_declaration=True)

if (sys.argv[3] == '2'):   # xml to csv  convet xml to pandas dataframes then create a csv file with using these dataframes 

 def intr_1(xml_doc):             # i took the sample function from this source : https://www.youtube.com/watch?v=WWgiRkvl1Ws&t=261s
     attr = xml_doc.attrib        # this function parces xml to one column with header name , so i used it for my all headers.
     for xml in xml_doc.iter('university') :
        doc_dict = attr.copy()
        doc_dict.update(xml.attrib)        
        yield doc_dict        
 def intr_2(xml_doc):
     attr = xml_doc.attrib 
     for xml in xml_doc.iter('item') :
        doc_dict = attr.copy()
        doc_dict.update(xml.attrib)        
        yield doc_dict      
 def intr_3(xml_doc):
    attr = xml_doc.attrib 
    for xml in xml_doc.iter('name') :
       doc_dict = attr.copy()
       doc_dict.update(xml.attrib)
       doc_dict['program'] = xml.text        
       yield doc_dict         
 def intr_4(xml_doc):
     attr = xml_doc.attrib 
     for xml in xml_doc.iter('period') :
        doc_dict = attr.copy()
        doc_dict.update(xml.attrib)
        doc_dict['period'] = xml.text        
        yield doc_dict 
 def intr_5(xml_doc):
     attr = xml_doc.attrib 
     for xml in xml_doc.iter('quota') :
        doc_dict = attr.copy()
        doc_dict.update(xml.attrib)
        doc_dict['quota'] = xml.text        
        yield doc_dict 
 def intr_6(xml_doc):
     attr = xml_doc.attrib 
     for xml in xml_doc.iter('field') :
        doc_dict = attr.copy()
        doc_dict.update(xml.attrib)
        doc_dict['type_of_score'] = xml.text        
        yield doc_dict 
 def intr_7(xml_doc):
     attr = xml_doc.attrib 
     for xml in xml_doc.iter('last_min_score') :
        doc_dict = attr.copy()
        doc_dict.update(xml.attrib)
        doc_dict['last_year_min_score'] = xml.text        
        yield doc_dict 
 def intr_8(xml_doc):
     attr = xml_doc.attrib 
     for xml in xml_doc.iter('grant') :
        doc_dict = attr.copy()
        doc_dict.update(xml.attrib)
        doc_dict['grant'] = xml.text        
        yield doc_dict 

 etree = ET.parse(sys.argv[1])
 df_1 = pd.DataFrame(list(intr_1(etree.getroot())))  #called my  functions one by one for each header (column of data)
 df_2 = pd.DataFrame(list(intr_2(etree.getroot())))
 df_3 = pd.DataFrame(list(intr_3(etree.getroot())))
 df_4 = pd.DataFrame(list(intr_4(etree.getroot())))
 df_5 = pd.DataFrame(list(intr_5(etree.getroot())))
 df_6 = pd.DataFrame(list(intr_6(etree.getroot())))
 df_7 = pd.DataFrame(list(intr_7(etree.getroot())))
 df_8 = pd.DataFrame(list(intr_8(etree.getroot())))
 df_1['faculty'] = df_2['faculty']
 df_1['id'] = df_2['id']                            # i added my columns one by one to my dataframe.After my final updated dataframe i created my csv with that dataframe
 df_1['second'] = df_3['second']
 df_1['lang'] = df_3['lang']
 df_1['program'] = df_3['program']
 df_1['period'] = df_4['period']
 df_1['spec'] = df_5['spec']
 df_1['quota'] = df_5['quota']
 df_1['type_of_score'] = df_6['type_of_score']
 df_1['order'] = df_7['order']
 df_1['last_year_min_score'] = df_7['last_year_min_score']
 df_1['grant'] = df_8['grant'] 
 df_1.to_csv(sys.argv[2],sep=';',encoding='UTF-8',index=False)

if (sys.argv[3] == '3'):  # xml to json  convert xml to pandas dataframes then create a json file with using these dataframes

 def intr_1(xml_doc):
     attr = xml_doc.attrib 
     for xml in xml_doc.iter('university') :
        doc_dict = attr.copy()
        doc_dict.update(xml.attrib)        
        yield doc_dict        
 def intr_2(xml_doc):
     attr = xml_doc.attrib 
     for xml in xml_doc.iter('item') :
        doc_dict = attr.copy()
        doc_dict.update(xml.attrib)        
        yield doc_dict      
 def intr_3(xml_doc):
    attr = xml_doc.attrib 
    for xml in xml_doc.iter('name') :
       doc_dict = attr.copy()
       doc_dict.update(xml.attrib)
       doc_dict['program'] = xml.text        
       yield doc_dict         
 def intr_4(xml_doc):
     attr = xml_doc.attrib 
     for xml in xml_doc.iter('period') :
        doc_dict = attr.copy()
        doc_dict.update(xml.attrib)
        doc_dict['period'] = xml.text        
        yield doc_dict 
 def intr_5(xml_doc):
     attr = xml_doc.attrib 
     for xml in xml_doc.iter('quota') :
        doc_dict = attr.copy()
        doc_dict.update(xml.attrib)
        doc_dict['quota'] = xml.text        
        yield doc_dict 
 def intr_6(xml_doc):
     attr = xml_doc.attrib 
     for xml in xml_doc.iter('field') :
        doc_dict = attr.copy()
        doc_dict.update(xml.attrib)
        doc_dict['type_of_score'] = xml.text        
        yield doc_dict 
 def intr_7(xml_doc):
     attr = xml_doc.attrib 
     for xml in xml_doc.iter('last_min_score') :
        doc_dict = attr.copy()
        doc_dict.update(xml.attrib)
        doc_dict['last_year_min_score'] = xml.text        
        yield doc_dict 
 def intr_8(xml_doc):
     attr = xml_doc.attrib 
     for xml in xml_doc.iter('grant') :
        doc_dict = attr.copy()
        doc_dict.update(xml.attrib)
        doc_dict['grant'] = xml.text        
        yield doc_dict 

 etree = ET.parse(sys.argv[1])
 df_1 = pd.DataFrame(list(intr_1(etree.getroot())))
 df_2 = pd.DataFrame(list(intr_2(etree.getroot())))
 df_3 = pd.DataFrame(list(intr_3(etree.getroot())))
 df_4 = pd.DataFrame(list(intr_4(etree.getroot())))
 df_5 = pd.DataFrame(list(intr_5(etree.getroot())))
 df_6 = pd.DataFrame(list(intr_6(etree.getroot())))
 df_7 = pd.DataFrame(list(intr_7(etree.getroot())))
 df_8 = pd.DataFrame(list(intr_8(etree.getroot())))
 df_1['faculty'] = df_2['faculty']
 df_1['id'] = df_2['id']
 df_1['second'] = df_3['second']
 df_1['lang'] = df_3['lang']
 df_1['program'] = df_3['program']
 df_1['period'] = df_4['period']
 df_1['spec'] = df_5['spec']
 df_1['quota'] = df_5['quota']
 df_1['type_of_score'] = df_6['type_of_score']
 df_1['order'] = df_7['order']
 df_1['last_year_min_score'] = df_7['last_year_min_score']
 df_1['grant'] = df_8['grant']  

 main_dict = df_1.to_dict()  # here i have some code for prettifying my json a bit. I made some changes on this code :https://stackoverflow.com/a/58620115
 datalist = []                         
 for c in range(df_1.shape[0]):
    subd = {}
    for k,v in main_dict.items():
        subd[k] = v[c]    
    datalist.append(subd) 
 with open(sys.argv[2],'w') as f:   
     json.dump(datalist,f,indent=9,ensure_ascii= False) 

 
if (sys.argv[3] == '4'):       # json to xml  first convert json to pandas dataframe then use dataframe to create xml
 with open(sys.argv[1]) as f:
  data = json.load(f) 
  df = DataFrame(data) 
  json_to_df = df[['uType','name','faculty','id','program','lang','second','grant','period','type_of_score','quota','spec','order','last_year_min_score']]
  # reordering headers because after csv_to_xml and xml_to_dataframe my headers's order changed. So ı have to reoder my headers for same xml format

  xml_doc = ET.Element('departments')
  for index,row in json_to_df.iterrows():
    university = ET.SubElement(xml_doc,'university',uType=str(json_to_df.iloc[index,0]),name=str(json_to_df.iloc[index,1]))
    item = ET.SubElement(university,'item',faculty=str(json_to_df.iloc[index,2]),id=str(json_to_df.iloc[index,3]))
    name = ET.SubElement(item,'name',second=str(json_to_df.iloc[index,6]),lang=str(json_to_df.iloc[index,5])).text =str(json_to_df.iloc[index,4])
    period = ET.SubElement(item,'period').text=str(json_to_df.iloc[index,8])
    quota = ET.SubElement(item,'quota',spec=str(json_to_df.iloc[index,11])).text=str(json_to_df.iloc[index,10])
    field = ET.SubElement(item,'field').text=str(json_to_df.iloc[index,9])
    last_min_score = ET.SubElement(item,'last_min_score',order=str(json_to_df.iloc[index,12])).text=str(json_to_df.iloc[index,13])
    grant = ET.SubElement(item,'grant').text=str(json_to_df.iloc[index,7])

  def prettify(element, indent='  '):  # I took ' prettify' function  and some other codes for building xml  from this source :https://www.youtube.com/watch?v=QiTMhvI4WrQ
                       
      queue = [(0, element)]  # (level, element)   
      while queue:
          level, element = queue.pop(0)
          children = [(level + 1, child) for child in list(element)]
          if children:
              element.text = '\n' + indent * (level+1)  # for child open
          if queue:
              element.tail = '\n' + indent * queue[0][0]  # for sibling open
          else:
              element.tail = '\n' + indent * (level-1)  # for parent close
          queue[0:0] = children  # prepend so children come before siblings

  prettify(xml_doc)
  tree = ET.ElementTree(xml_doc)
  tree.write(sys.argv[2],encoding='UTF-8',xml_declaration=True) 



if (sys.argv[3] == '5'): # csv to json first parse csv to pandas dataframe then create json with dataframe
 df = pd.read_csv(sys.argv[1],delimiter=';')
 df = df.fillna('') # converting NaN which is causes errors to ''

 main_dict = df.to_dict()  # here i have some code for prettifying my json a bit. I made some changes on this code :https://stackoverflow.com/a/58620115
 datalist = []
 for c in range(df.shape[0]):
     subd = {}
     for k,v in main_dict.items():
         subd[k] = v[c]    
     datalist.append(subd) 
 with open(sys.argv[2],'w') as f:   
     json.dump(datalist,f,indent=9,ensure_ascii= False)

if(sys.argv[3] == '6'):  # json to csv first parse json to pandas dataframe then create csv with dataframe
 with open(sys.argv[1]) as f:
   data = json.load(f) 
   json_to_df = DataFrame(data) 
 
 json_to_df.to_csv(sys.argv[2],sep=';',encoding='UTF-8',index=False)



if(sys.argv[3]=='7'):                  # This code is from our classroom
                                       #  validate.py       # Its for validating xml by using our XML_VALIDATE.xsd
 doc = etree.parse(sys.argv[1])
 root = doc.getroot()
 xmlschema_doc = etree.parse(sys.argv[2])
 xmlschema = etree.XMLSchema(xmlschema_doc)   
 doc = etree.XML(etree.tostring(root))
 validation_result = xmlschema.validate(doc)
 print(validation_result)
 xmlschema.assert_(doc)
