from urllib.parse import urlparse,urljoin,urlunparse,ParseResult
p1=urlparse('//www.cwi.nl:80/%7Eguido/Python.html')
print('1',p1)
p2=urlparse('www.cwi.nl/%7Eguido/Python.html')
print('2',p2)
p3=urlparse('help/Python.html')
print('3',p3)

url="https://tenant.51datakey.com/carrier/mxreport_data?data=aX92rOy5T06Q%2FSuP0eVrRE1IibeVkuuE3E5AaZD8Styw83qrUN0BqUo2QYYp1cpbfh2HNnVVdfEmtTqs%2F44PNZWGMERQnPTFCrW873BDR4T3hmK61GFdbQfYPjCiFZeXSURqsDNiXEA10OV9hT5C%2BfEtDIj%2FZeFeWRflHihrRZ4B31X%2FIqJawW2MCHmGoH2M"
p4=urlparse(url)
print('p4',p4)
# print('query',p4.query)
# print('netloc',p4.netloc)

url_data =url.replace('mxreport_data','mxreport_data/reportBasic')
print('url_data',url_data)

url2='https://tenant.51datakey.com/carrier/mxreport_data/reportBasic?data=aX92rOy5T06Q%2FSuP0eVrRE1IibeVkuuE3E5AaZD8Styw83qrUN0BqUo2QYYp1cpbfh2HNnVVdfEmtTqs%2F44PNZWGMERQnPTFCrW873BDR4T3hmK61GFdbQfYPjCiFZeXSURqsDNiXEA10OV9hT5C%2BfEtDIj%2FZeFeWRflHihrRZ4B31X%2FIqJawW2MCHmGoH2M&contact=&mobile=13149357244&taskId=d8f40720-0e4e-11e9-9f12-00163e0f4b67&inputliveaddress='
p5=urlparse(url2)
print('p5',p5)

print('urlunparse',urlunparse(("https","i.cnblogs.com","/EditPosts.aspx","","opt=1","")))


'''
1 ParseResult(scheme='', netloc='www.cwi.nl:80', path='/%7Eguido/Python.html', params='', query='', fragment='')
2 ParseResult(scheme='', netloc='', path='www.cwi.nl/%7Eguido/Python.html', params='', query='', fragment='')
3 ParseResult(scheme='', netloc='', path='help/Python.html', params='', query='', fragment='')
p4 ParseResult(scheme='https', netloc='tenant.51datakey.com', path='/carrier/mxreport_data', params='', query='data=aX92rOy5T06Q%2FSuP0eVrRE1IibeVkuuE3E5AaZD8Styw83qrUN0BqUo2QYYp1cpbfh2HNnVVdfEmtTqs%2F44PNZWGMERQnPTFCrW873BDR4T3hmK61GFdbQfYPjCiFZeXSURqsDNiXEA10OV9hT5C%2BfEtDIj%2FZeFeWRflHihrRZ4B31X%2FIqJawW2MCHmGoH2M', fragment='')
query data=aX92rOy5T06Q%2FSuP0eVrRE1IibeVkuuE3E5AaZD8Styw83qrUN0BqUo2QYYp1cpbfh2HNnVVdfEmtTqs%2F44PNZWGMERQnPTFCrW873BDR4T3hmK61GFdbQfYPjCiFZeXSURqsDNiXEA10OV9hT5C%2BfEtDIj%2FZeFeWRflHihrRZ4B31X%2FIqJawW2MCHmGoH2M
netloc tenant.51datakey.com
'''

