import json
with open('data/review_train.json','r') as r:
    data=r.read()
data=data.replace('}','},')
data='['+data+']'
with open ('data/review_formatted.json','w') as r:
    r.write(data)

