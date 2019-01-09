import json
path='/Users/ozintel/Downloads/Tsl_python_progect/local_ml/mihua/mihua/data/content.html'
import pandas as pd

# Reading data back
with open(path, 'r') as f:
    data = json.load(f)
    print(data)
    print(data.keys())
    for key in data.keys():
        print(data[key])
    print('一共页数',data['page']['pages'])

    print(data['data'])
    for each in data['data']:
        print('each',each)
    df=pd.DataFrame(data['data'])
    print('df.head',df.head())