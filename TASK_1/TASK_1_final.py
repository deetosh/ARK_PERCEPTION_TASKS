import cv2 as cv
import numpy as np
from math import pi
import decimal
import math

def template_Match(img,template):
    row= int(img.shape[0]-template.shape[0]+1)
    col= int(img.shape[1]-template.shape[1]+1)
    arr = [[0] * col for _ in range(row)]
    total= template.shape[0]*template.shape[1]
    h=template.shape[0]
    w=template.shape[1]
    maxi=-1
    index_x=0
    index_y=0
    i=0
    j=0
    while i <row:
        j=0
        while j <col:
            temp= img[i:i+h,j:j+w]-template 
            count=total-cv.countNonZero(temp)
            if count>maxi:
                maxi=count
                index_x=i
                index_y=j
            j+=1
        i+=1    
    return (index_x,index_y)

def compute_pi(n):                   # compute the digits of pi for finding the noise in pi_image
  decimal.getcontext().prec = n + 3
  decimal.getcontext().Emax = 999999999
  
  C = 426880 * decimal.Decimal(10005).sqrt()
  K = decimal.Decimal(6)
  M = decimal.Decimal(1)
  X = decimal.Decimal(1)
  L = decimal.Decimal(13591409)
  S = L
  for i in range(1, n+3):
    M = decimal.Decimal(M* ((1728*i*i*i)-(2592*i*i)+(1104*i)-120)/(i*i*i))
    L = decimal.Decimal(545140134+L)
    X = decimal.Decimal(-262537412640768000*X)
    S += decimal.Decimal((M*L) / X)
    
  return str(C/S)[:-2] # Pi is C/S

s= compute_pi(2499)
pi_img = cv.imread('photos/pi_image.png')

height= pi_img.shape[0]
width= pi_img.shape[1]
a = [0] * 2501
filter = [0] * 4

count=0      # putting the digits of pi in array a
for i in range(height):
    for j in range(width):
        k = int(pi_img[i,j][0]/10)
        a[count]=k
        if count==0:
           a[count+1]='.'
           count+=1
        count+=1

count=0
for i in range(2501):
   if i!=1 and a[i]-int(s[i])!=0:
      filter[count]=int(int(s[i])*10*pi)
      count+=1

filter_values = sorted(filter, reverse=True)
print("the filter values are: ",end="")
print(filter_values)

img2=cv.imread('photos/artwork_picasso.png',cv.IMREAD_GRAYSCALE)
w,h= img2.shape[1],img2.shape[0]

collage=cv.imread('photos/collage.png',cv.IMREAD_GRAYSCALE)
# cv.imshow('collage',collage)
  
i=0
j=0
while i<h:
   j=0
   while j<w:         
         img2[i][j]=filter_values[1]^((img2[i][j])) 
         
      
         img2[i+1][j]=((img2[i+1][j]^filter_values[2]))  #
         

         img2[i][j+1]=(img2[i][j+1])^filter_values[1] + 224
         
     
         img2[i+1][j+1]=(img2[i+1][j+1]) 
         
         j+=2
   i+=2

# img2=cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
cv.imshow('found',img2)

res=template_Match(collage,img2)
password= int((res[0]+res[1])*pi)
print("password= "+ str(password))

cv.waitKey(0)
