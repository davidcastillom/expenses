mx = lambda x,y: x if x>y else y

print(mx(8,10))


n=[10,9,8,7,6,5,4,3,2,1]
x=map(lambda x:x**2,n)

print(list(x))


y=filter(lambda x:x==10,n)
print(list(y))


for i in range(1,5):
    print("elemento {} tiene valor {}".format(i, n[i]))
i=0
while i<=5:
    print(n[i], i)
    i += 1

a,b = 0,1
for i in range(0, 10):
    print(a)
    a,b = b,b+a


a=0
b=1
for i in range(0,10):
    print("a {}  b {}".format(a,b))
    c=a+b
    a=b
    b=c


    a=['1','2','3']
    print("-".join(a))

    print( "th2 {}") side
