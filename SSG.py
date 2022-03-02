# -*- coding: utf-8 -*-


"""
Created on Sun Dec 29 16:43:34 2019

@author: chin
"""

#All Material set
M=['AA','BB','CC','DD','EE','FF','GG','HH','JJ','KK','LL']

#Product/Output Sets
P=['AA']

#Raw Material Sets/Input Sets
R=['EE','GG','JJ','KK','LL']


#Operating Unit Sets
O=[ \
   [['CC'],['AA','FF']], \
   [['DD'],['AA','BB']], \
   [['EE','FF'],['CC']], \
   [['FF','GG'],['CC','DD']], \
   [['GG','HH'],['DD']], \
   [['JJ'],['FF']], \
   [['LL','KK'],['HH']], \
   ]

#print(O)

#Operating units that output M
def phiminus(M,O):
    results=[]
    for i in M:
        for j in O:
            for k in j[1]:
                if k==i:
                    results.append(j)
    return results
                    #O.remove(j)
                    
#Operating units that input M
def phiplus(M,O):
    results=[]
    for i in M:
        for j in O:
            for k in j[0]:
                if k==i:
                    results.append(j)
    return results

#Input materials to operating units O
def inputO(O):
    results=[]
    result1=[]
    for i in O:
        for j in i[0]:
            results.append(j)
    
    while results!=[]:
        first=results.pop(0)
        check=[]
        for k in range(0,len(results)):
            check.extend([first!=results[k]])
        
        check1=all(elem==True for elem in check)
        if check1:
            result1.append(first)
    return result1


c=[[['E','F'],['C']], \
   [['F','G'],['C','D']]]

r=inputO(c)
r1=[]
#
#
#            
#    
#            
#r1=[i for i in r if i not in r1]

#Output materials to operating units o
def outputO(O):
    results=[]
    result1=[]
    for i in O:
        for j in i[1]:
            results.append(j)
    while results!=[]:
        first=results.pop(0)
        check=[]
        for k in range(0,len(results)):
            check.extend([first!=results[k]])
        
        check1=all(elem==True for elem in check)
        if check1:
            result1.append(first)
    return result1   
    #results=[i for i in results if i not in results]

#P.remove(M)
#outputO(O)
    
#Powerset function, but using list      
def powerset(A):
    if A == []:
        return [[]]
    a = A[0]
    incomplete_pset = powerset(A[1:])
    rest = []
    for set in incomplete_pset:
        rest.append([a] + set)
    return rest + incomplete_pset

print(powerset(['P1','P2','P3','P4','P5']))
#delta(['A','B'])
#delta([])



def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 


def SSG(Pn,R,O,Mn=[[]],delta=[],deltb=[],result=[]):
    Prod=Pn
    m=Mn

    if Prod:    
        for x in Prod:
            C=[]
            C=powerset(phiminus([x],O))
            #C.append(C.pop(0))
            C=[i for i in C if i != [] ]

#            C=phiminus([x],O)
#            C=[[i] for i in C]            
            for c in C:
                T=[]
                T=[i for i in phiminus([x],O) if i not in c]                
                Check1=[]
                Check2=[]
                for y in m:
                    G=[]
                    G=[i for i in phiminus([y],O) if i not in delta]
                    Check1.extend(intersection(T,delta)) 
                    Check2.extend(intersection(c,G))                    
                    res1=all(ele==[] for ele in Check1)
                    res2=all(ele==[] for ele in Check2)
                    
                if  res1 and res2:
                    #delta.extend(c)
                    #deltb.append([x,c])
                    if len(c)>=2:
                        delta.extend(c)
                    else:
                        delta.extend(c)

                    deltb.extend([x,c])
                    
                    matin=[]
                    #matin.append(inputO(c))  
                    matin=[i for i in inputO(c)]  
                    
                    red=[]
                    red.extend(i for i in R if i != red)
                    red.extend(i for i in m if i != red and i!= [])
                    red.extend(i for i in [x] if i != red)  
                    
                    #Prod.extend(i for i in matin if i not in Prod)
                    Prod1=[]
                    Prod1=[i for i in Prod  ]
                    Prod1=Prod1+[i for i in matin if i not in Prod1 ]
                    Prod1=[i for i in Prod1 if i not in red]  
                    
                    #m.extend(i for i in x if i not in m)
                    m=m+[i for i in [x] if i not in m]
                    m=[i for i in m if i!=[]] 

                    
                    SSG(Prod1,R,O,m,delta,deltb,result)
                    if m!=[]:
                        m.pop()
                    #if Prod!=[]:
                        #Prod.pop()
                    if delta!=[]:
                        delta.pop()
                        if len(c)>=2:
                            delta.pop()
                    if deltb!=[]:
                        deltb.pop()
                        deltb.pop()
            return result
    else:
        rr=[]
        rr=[i for i in deltb]
        result.append(rr)
#        results=[i for i ]
    return result
                      
ress=SSG(P,R,O)

print(len(ress))
print(ress)
   
