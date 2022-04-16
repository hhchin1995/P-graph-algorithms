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


def SSG(Pn, R, O, max_sol=1000, mutual=[], Mn=[[]], delta=[], deltb=[], result=[], result2=[]):
    Prod = Pn
    m = Mn
    if Prod:
        for x in Prod:
            C = []
            C = powerset(phiminus([x], O))
            # C.append(C.pop(0))
            C = [i for i in C if i != []]

            #            for me in mutual:
            #                C=[i for i in C if i != me] # Exclude mutual exclusion set

            #            C=phiminus([x],O)
            #            C=[[i] for i in C]
            for c in C:
                T = []
                T = [i for i in phiminus([x], O) if i not in c]
                Check1 = []
                Check2 = []
                for y in m:
                    G = []
                    G = [i for i in phiminus([y], O) if i not in delta]
                    Check1.extend(intersection(T, delta))
                    Check2.extend(intersection(c, G))
                    res1 = all(ele == [] for ele in Check1)
                    res2 = all(ele == [] for ele in Check2)

                if res1 and res2:
                    # delta.extend(c)
                    # deltb.append([x,c])

                    delta.extend(c)

                    deltb.extend([x, c])

                    matin = []
                    # matin.append(inputO(c))
                    matin = [i for i in inputO(c)]

                    red = []
                    red.extend(i for i in R if i != red)
                    red.extend(i for i in m if i != red and i != [])
                    red.extend(i for i in [x] if i != red)

                    # Prod.extend(i for i in matin if i not in Prod)
                    Prod1 = []
                    Prod1 = [i for i in Prod]
                    Prod1 = Prod1 + [i for i in matin if i not in Prod1]
                    Prod1 = [i for i in Prod1 if i not in red]

                    # m.extend(i for i in x if i not in m)
                    m = m + [i for i in [x] if i not in m]
                    m = [i for i in m if i != []]

                    SSG(Prod1, R, O, max_sol, mutual, m, delta, deltb, result, result2)
                    if m != []:
                        m.pop()
                    # if Prod!=[]:
                    # Prod.pop()
                    if delta != []:
                        for c_count in range(len(c)):
                            delta.pop()
                            c_count = c_count + 1
                    #                        if len(c)>=2:
                    #                            delta.pop()
                    if deltb != []:
                        deltb.pop()
                        deltb.pop()
            return result, result2
    else:
        # Exclude mutual exclusion set
        Check3 = []
        for x in range(len(mutual)):
            mutual_x = []
            mutual_x.extend(me for me in mutual[x])

            Check3.extend([intersection(mutual_x, delta) == mutual_x])
        res3 = all(ele == 0 for ele in Check3)
        rr = []
        rr2 = []

        if res3:  # If results contain the mutual exclusion set, ignore it
            rr = [i for i in deltb]

            rr2 = [i for i in delta]

        if len(result) >= max_sol or not res3:
            return
        else:
            result.append(rr)
            result2.append(rr2)
    return result, result2


ress = SSG(P, R, O, 10000, ME)

Solutions = {}

for i in range(0, len(ress[0])):
    key = 'Solution # ' + str(i + 1)
    Solutions[key] = ress[0][i]

print(Solutions)

Solutions2 = {}

for i in range(0, len(ress[1])):
    key = 'Solution # ' + str(i + 1)
    Solutions2[key] = ress[1][i]

print(Solutions2)

print(len(ress[0]))
print(len(ress[1]))
# print(ress)

   
