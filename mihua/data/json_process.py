import json
import xlsxwriter
'''content'''

path='/Users/ozintel/Downloads/Tsl_python_progect/local_ml/mihua/mihua/data/contacts.html'
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

def process_contacts(path):
    with open(path, 'r') as f:
        data = json.load(f)
        print(data)
        print('data',data['data'])
        dl=data['data']['list']
        print('data list',dl )
        df=pd.DataFrame(dl)
        print('shape',df.shape)
        print('df',df.head())
        # print('df.T', df.head().T)
        each_line = {}
        for index,each in enumerate(dl):
            print('dl each',each['name'],each['phone'])
            each_line['name{}'.format(index)]=each['name']
            each_line['phone{}'.format(index)] = each['phone']

        print('each_line',each_line)
        df2=pd.DataFrame([each_line])
        print(df2)
        df2.to_excel(
            '/Users/ozintel/Downloads/Tsl_python_progect/local_ml/mihua/mihua/data/my_order_contacts_temp.xlsx',
            index=False,
        engine='xlsxwriter')

        # writer = pd.ExcelWriter('file.xlsx')
        # df2.to_excel(writer, sheet_name='Sheet1')
        # writer.save()
        #
        # out = pd.ExcelWriter('output.xls')
        # df2.to_excel(out)
        # out.save()



        for each in dl:
            print('each',each)

        a={'id': 4502138, 'userId': 89685, 'name': '油漆店', 'phone': '13606835997'}
        b= {'id': 4502139, 'userId': 89685, 'name': '王文琴', 'phone': '15868326980'}
        c={}
        c.update(a)
        print('c1',c)
        c.update(b)
        print('c2',c)
        print('合并',dict(a,**b))














if __name__=='__main__':
    # process_detail_json(path)
    # process_collect_json(path)
    process_contacts(path)