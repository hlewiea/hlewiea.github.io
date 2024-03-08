# -*- coding: utf-8 -*-
# python学习
## 1.1 基础
### 1.1.1 输入输出
~~~ python
print('hello, world')
name = input()
print('hello,',name)
# 4空格缩进
x = 10_0000_0000 # 10000000000 
y = 0xa1b2_c3d4
z = 1.23e9
str1 = 'I\'m \"OK\"!' # I'm "OK"!
# 转义\, 不转义: r'不转义部分'
# '''...line1...line2...line3''',
# print(r'''hello,\n world''')

bool1 = True; # false, and or not
# 空值 None
# 动态语言可以反复赋不同类型的值
# / 结果是浮点数 // 结果是整数 %
~~~
### 1.1.2 字符串
ord()函数获取字符的整数表示
chr()函数把编码转换为对应的字符
encode/decode : errors='ignore'忽略decode无效的字节
长度len()
// 告诉Linux/OS X系统，这是一个Python可执行程序，Windows系统会忽略这个注释；
#!/usr/bin/env python3
// 告诉Python解释器，按照UTF-8编码读取源代码,申明了UTF-8编码并不意味着你的.py文件就是UTF-8编码的，
// 必须并且要确保文本编辑器正在使用UTF-8 without BOM编码：
格式化　%d %s %x %f 整数字符串十六进制浮点　相应%%表示%
.format() 传入占位符
#-*- coding: utf-8 -*-
~~~python
>>> ord('A')
65
>>> ord('中')
20013
>>> chr(66)
'B'
>>> chr(25991)
'文'
>>> '\u4e2d\u6587'
'中文'
x = b'ABC' # bytes类型,每个字符只占用一字节
>>> 'ABC'.encode('ascii')
b'ABC'
>>> '中文'.encode('utf-8')
b'\xe4\xb8\xad\xe6\x96\x87'
>>> b'ABC'.decode('ascii')
'ABC'
>>> b'\xe4\xb8\xad\xe6\x96\x87'.decode('utf-8')
'中文'
# 如果bytes中只有一小部分无效的字节，可以传入errors='ignore'忽略错误的字节：
>>> b'\xe4\xb8\xad\xff'.decode('utf-8', errors='ignore')
'中'
>>> 'Age: %s. Gender: %s' % (25, True)
'Age: 25. Gender: True'
>>> 'growth rate: %d %%' % 7
'growth rate: 7 %'
>>> 'Hello, {0}, 成绩提升了 {1:.1f}%'.format('小明', 17.125)
'Hello, 小明, 成绩提升了 17.1%'

>>> r = 2.5
>>> s = 3.14 * r ** 2
>>> print(f'The area of a circle with radius {r} is {s:.2f}') #2f 保留2位小数
The area of a circle with radius 2.5 is 19.62
~~~
### 1.1.3　list 和　tuple
list: len [0] [-1] append('') insert(1,'') pop最后一个 pop(i)　

~~~python
>>> classmates = ['Michael', 'Bob', 'Tracy']
>>> classmates
['Michael', 'Bob', 'Tracy']
>>> len(classmates)
3
>>> classmates[0]
'Michael'
>>> classmates[-1]
'Tracy'
>>> classmates.append('Adam')
>>> classmates
['Michael', 'Bob', 'Tracy', 'Adam']
>>> classmates.insert(1, 'Jack')
>>> classmates
['Michael', 'Jack', 'Bob', 'Tracy', 'Adam']
>>> classmates.pop()
'Adam'
>>> classmates
['Michael', 'Jack', 'Bob', 'Tracy']
>>> L = ['Apple', 123, True]
>>> s = ['python', 'java', ['asp', 'php'], 'scheme']
>>> len(s)
4
# 要拿到'php'可以写s[2][1]
>>> L = []
>>> len(L)
0
~~~
tuple: 一旦初始化就不能修改,它也没有append()，insert()这样的方法。
其他获取元素的方法和list是一样的，你可以正常地使用classmates[0]，classmates[-1]，但不能赋值成另外的元素。
可以往里面加list元素使其可变
~~~python
>>> classmates = ('Michael', 'Bob', 'Tracy')
>>> t = (1, 2)
>>> t
(1, 2)
>>> t = ()
>>> t
()
>>> t = (1) # 变成小()
>>> t
1
>>> t = (1,)
>>> t
(1,)
>>> t = ('a', 'b', ['A', 'B'])
>>> t[2][0] = 'X'
>>> t[2][1] = 'Y'
>>> t
('a', 'b', ['X', 'Y'])
~~~
### 1,1,4 判断
if 它是从上往下判断，如果在某个判断上是True，把该判断对应的语句执行后，就忽略掉剩下的elif和else
for range while
~~~python
age = 3
if age >= 18:
    print('adult')
elif age >= 6:
    print('teenager')
else:
    print('kid')

s = input('birth: ')
birth = int(s)
if birth < 2000:
    print('00前')
else:
    print('00后')

names = ['Michael', 'Bob', 'Tracy']
for name in names:
    print(name)
>>> list(range(5))
[0, 1, 2, 3, 4]
# 循环内部变量n不断自减，直到变为-1时，不再满足while条件，循环退出。
sum = 0
n = 99
while n > 0:
    sum = sum + n
    n = n - 2
print(sum)
~~~
### 1.1.5 dict set
dict 
~~~python
>>> d = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
>>> d['Michael']
95
>>> d['Adam'] = 67
>>> d['Adam']
67
# 多次对一个key放入value，后面的值会把前面的值冲掉
# 要避免key不存在的错误，有两种办法，一是通过in判断key是否存在
>>> 'Thomas' in d
False
# 二是通过dict提供的get()方法，如果key不存在，可以返回None，或者自己指定的value：
>>> d.get('Thomas')
>>> d.get('Thomas', -1)
-1
# 删除一个key，用pop(key)方法
>>> d.pop('Bob')
75
>>> d
{'Michael': 95, 'Tracy': 85}
# 通过key计算位置的算法称为哈希算法（Hash）。
# 作为key的对象就不能变。在Python中，字符串、整数等都是不可变的，因此，可以放心地作为key。而list是可变的，就不能作为key：
~~~ 
set: set和dict类似，也是一组key的集合，但不存储value。由于key不能重复，所以，在set中，没有重复的key。
add remove & | 
~~~python
# 要创建一个set，需要提供一个list作为输入集合,重复元素在set中自动被过滤：：
>>> s = set([1, 1, 2, 2, 3, 3])
>>> s
{1, 2, 3}
>>> s.add(4)
>>> s
{1, 2, 3, 4}
>>> s.remove(4)
>>> s
{1, 2, 3}
>>> s1 = set([1, 2, 3])
>>> s2 = set([2, 3, 4])
>>> s1 & s2
{2, 3}
>>> s1 | s2
{1, 2, 3, 4}
~~~
set和dict的唯一区别仅在于没有存储对应的value，但是，set的原理和dict一样，所以，同样不可以放入可变对象，因为无法判断两个可变对象是否相等，也就无法保证set内部“不会有重复元素”。
不可变对象
~~~python
>>> a = 'abc'
>>> b = a.replace('a', 'A') #创建新字符串返回
>>> b
'Abc'
>>> a
'abc'
~~~
### 1.1.6　函数
~~~python
x = 15
s = area_of_circle(x)
max()
min()
abs()
int()
float()
str()
bool()
hex()
def my_abs(x):
    if x >= 0:
        return x
    else:
        return -x
# 如果你已经把my_abs()的函数定义保存为abstest.py文件了，那么，可以在该文件的当前目录下启动Python解释器，用from abstest import my_abs来导入my_abs()函数，注意abstest是文件名（不含.py扩展名）：

# 如果想定义一个什么事也不做的空函数，可以用pass语句：
def nop():
    pass
# 数据类型检查可以用内置函数isinstance()实现：
def my_abs(x):
    if not isinstance(x, (int, float)):
        raise TypeError('bad operand type')
    if x >= 0:
        return x
    else:
        return -x

# 函数可以返回多个值（即一个tuple）
import math

def move(x, y, step, angle=0):
    nx = x + step * math.cos(angle)
    ny = y - step * math.sin(angle)
    return nx, ny
>>> r = move(100, 100, 60, math.pi / 6)
>>> print(r)
(151.96152422706632, 70.0)
~~~
默认参数存在xz
