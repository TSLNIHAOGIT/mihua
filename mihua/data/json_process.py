import json
'''content'''

path='/Users/ozintel/Downloads/Tsl_python_progect/local_ml/mihua/mihua/data/content.html'
import pandas as pd


def process_collect_json(path):
    # Reading data back
    with open(path, 'r') as f:
        data = json.load(f)
        print('data',data)
        print(data.keys())
        for key in data.keys():
            print(data[key])
        print('一共页数',data['page']['pages'])

        print('userId',data['data'][0]['userId'])

        for each in data['data']:
            print('each id',each['borrowUserId'])
        print(data['data'])
        for each in data['data']:
            print('each',each)
        df=pd.DataFrame(data['data'])
        print('df.head',df.head())
def process_detail_json(path):
    # Reading data back
    with open(path, 'r') as f:
        data = json.load(f)
        print(data)
        print(data.keys())
        for key in data.keys():
            print(data[key])

        all_contach_info=data['data']['userContactInfo']
        print(all_contach_info)

        for each in all_contach_info:
            print('each', each['name'],each['phone'],each['relation'])
        # df = pd.DataFrame(data['data'])
        # print('df.head', df.head())
if __name__=='__main__':
    # process_detail_json(path)
    process_collect_json(path)
