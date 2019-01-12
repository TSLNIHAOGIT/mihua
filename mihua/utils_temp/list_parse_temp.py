a={}
for each in ['a','b','c']:
    a[each]=each

print(a)

a = {'a':1,'b':2}
b = {'c':3}
d={'q':123}

# 方法1
new_dict = a
new_dict.update(b)
new_dict.update(d)
print('new_dict',new_dict)

# 方法2
# new_dict = dict(a.items()+b.items())

# 方法3(Pythonic)new_dict = dict(a, **b)