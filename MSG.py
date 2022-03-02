# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 16:43:34 2019

@author: chin
"""
#from docplex.mp.model import Model


#All Material set
M=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','Q','T','U','V']

#Product/Output Sets
P=['B']

#Raw Material Sets/Input Sets
R=['F','H','M','T']

#Operating Unit Sets
O=[ \
   [['C','D','F'],['A']], \
   [['D'],['B','G']], \
   [['E'],['B','U']], \
   [['F','G'],['C','D']], \
   [['G','H'],['D']], \
   [['H','I'],['E']], \
   [['J','K'],['E']], \
   [['M'],['G']], \
   [['N','Q'],['H']], \
   [['T','U'],['I']], \
   [['V'],['J']] \
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
#P.remove(M)
                    


#Maximal Structure Generation ALgorithms
def MSG(P,R,O):
    #Reduction algorithm
    O=[i for i in O if i not in phiminus(R,O)]
#    O.remove(phiminus(R,O)) #Remove the operating units that produce raw materials
    
    #########Updated Material sets
    M=[]
    M1=inputO(O)
    M2=outputO(O)
    
    M.extend(i for i in M1 if i not in M)
    M.extend(i for i in M2 if i not in M)
    ##########
    
    ######### All inlet materials but not raw materials, and not produced by any 'O' are excluded
    r=[]
    rr=[]
    
    rr.extend(i for i in M2 if i not in rr)
    rr.extend(i for i in R if i not in rr)
    
    r.extend(i for i in M1 if i not in r)
    r=[i for i in r if i not in rr]
    ##########
    
    while len(r)!=0:
        for x in r:
            M=[i for i in M if i != x]
            so=phiplus(x,O)
            O=[i for i in O if i not in so]
            
            #Because when 'so' removed, the output from 'so' might become inlet but not produced, 
            #so need to remove
            um=[]
            um=[i for i in outputO(so) if i not in um]
            um=[i for i in um if i not in outputO(O)]
            
            r.extend(um)
            r=[i for i in r if i !=x]
            
    check=any(elem in M for elem in P ) #Check if P is inside list M
    
    #Composition algorithm     
    if not check:
        print('No maximal structure')
        return
    else:
        p=P
        m=[]
        o=[]
        
        while len(p)!=0:
            mr=[]
            for x in p:
                mr.extend(x)
                m=m+[i for i in mr if i not in m]
                ox=phiminus(x,O)
                o=o+[i for i in ox if i not in o]
                
                p=p+[i for i in inputO(ox) if i not in p]
                #p.extend(inputO(ox))
                pr=[]+R+m
                p=[i for i in p if i not in pr]
                
        m.extend(i for i in inputO(o) if i not in m)
        m.extend(i for i in outputO(o) if i not in m)
    
    return [m,o]


def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 

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


def SSG(Pn,R,O,Mn=[[]],delta=[],deltb=[],result=[[]]):
    Prod=Pn
    m=Mn

    if Prod==[]:
        rr=[]
        rr=[i for i in deltb]
        result.append(rr)
#        results=[i for i ]
        return result
    else:    
        for x in Prod:
            C=[]
            C=powerset(phiminus(x,O))
            #C.append(C.pop(0))
            C=[i for i in C if i != []]            
            for c in C:
                T=[]
                T=[i for i in phiminus(x,O) if i not in c]                
                Check1=[]
                Check2=[]
                for y in m:
                    G=[]
                    G=[i for i in phiminus(y,O) if i not in delta]
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
                    red.extend(i for i in x if i != red)  
                    
                    #Prod.extend(i for i in matin if i not in Prod)
                    Prod1=[]
                    Prod1=[i for i in Prod if i ]
                    Prod1=Prod1+[i for i in matin if i not in Prod1 ]
                    Prod1=[i for i in Prod1 if i not in red]  
                    
                    #m.extend(i for i in x if i not in m)
                    m=m+[i for i in x if i not in m]
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
                    

res=[[]]
                    
M=MSG(P,R,O)[0]
O=MSG(P,R,O)[1]
p=[i for i in P]
res=SSG(P,R,O)

print(M)
print(len(res))


        

    


                    
        
    