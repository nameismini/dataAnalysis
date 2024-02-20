# By submitting this assignment, I agree to the following:
#  I do not lie, cheat, or steal, or tolerate those who do
#  I have not given or received any unauthorized aid on this assignment
#
# Name:           MiN
# section:        YOUR SECTION NUMBER
# Team:           N/A
# Assignment:     THE ASSIGNMENT NUMBER (e.g. Lab 1b-2)
# Date:           DAY MONTH YEAR ${now}

# %% <자료구조>
# list(순서O, 집합) []
mylist = []
mylist = ['1', '2', '3', '4', '5']
mylist = [[1, 2, 3], [4, 5, 6]]
mylist.append('')
# mylist.remove(1)
mylist[0:3]
# print(len(mylist))
print('list', mylist)

# tuple(순서O, 읽기 전용) (‘’,’’,’,’’)
mytuple = ()
mytuple = (1, 2, 3)
mytuple = (1, 2, (3, 4, 5))
print('tuple', mytuple[1:])

# set(순서X, 중복X, 집합)
myset = set()
myset.add('1')
myset.add('3')
myset.add('2')
myset.add('5')

print('set', myset)

# dict(key, value로 이루어진 사전형 집합) {‘aaa’:’a’, ‘bbb’:’b’} or mydict = dict()
mydict = dict()
mydict['apple'] = 123
mydict['apple']

mydict = {'aaa':'a', 'bbb':'b'}
print('dict', mydict)
print(type(mydict))



# %% <숫자형>

# 정수
a = 123
# 실수
a = 1.2
a = 4.24e-10 #4.24*10의10승
a = 4.24E10 #4.24*10의마이너스10승
# 8진수
a = 0o177  #숫자0 + 영문 오 소문자/대문자
# 16진수
a = 0x8ff  #0x로 시작하면 됨

# 사칙연산
3 ** 4   #제곱 3*3*3*3
7 % 3    #나눗셈후 나머지 반환
7 // 3   #나눗셈후 몫을 반환


#%%
a = '12341234 %10s' % 'hi'
a[2:]
