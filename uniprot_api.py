from urllib2 import Request, urlopen, URLError
import ast
'''
request = Request("website")


variable = urlopen("website")
response = variable.read()
body = response[value1:value2]
print body


variable = requests.get("website")
print variable.text[value1:value2]


body = {'Name': 'value1'}
response = requests.post("website", data=body)
'''


result = urlopen("http://www.broadinstitute.org/oncotator/mutation/7_55259515_55259515_T_G/")
response = result.read()
new_dict = ast.literal_eval(response)
polyphen = new_dict.get('dbNSFP_RadialSVM_pred')
print polyphen
