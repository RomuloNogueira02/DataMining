########################################################################################
#          A Recursive Frequent Itemset Discovery Algorithm in 100% pure Python        #
#          Created for the Data Mining Course @ DI/FCUL                                #
#          (c) Andre O. Falcao 2020-2022                                               #
########################################################################################

from functools import reduce
import pandas as pd

def GetTranspose(trs):
    #computes the transpose of a transaction dataset
    #Author: Andre O. Falcao (c) 2020-2022
    it_trs={}
    for c,tr in enumerate(trs):
        for i in tr:
            it_trs.setdefault(i,[]).append(c)
    for i in it_trs: it_trs[i]=set(it_trs[i])
    return it_trs


def MinSupportSets(cmb, min_supp, its, trs, supports, N, good_trans):
    #cmb is the current combination of items
    #min_supp is the minimum support required
    #its is the set of items not yet tested 
    #trs is the list for all transactions
    #supports corresponds to the list of itemsets with support > min_supp (it is actually a dict)
    for it in its-cmb:
        sit = {it}
        new_cmb= frozenset(cmb | sit)
        if new_cmb not in supports:
            if good_trans is None:
                new_trans = trs[it]
            else:
                new_trans = trs[it] & good_trans
            supp      = len(new_trans) / N
            if supp>=min_supp: 
                supports[new_cmb]=supp
                its0=its-sit
                if len(its0)>0:
                    MinSupportSets(new_cmb, min_supp, its0, trs, supports, N, new_trans)

def getAllItems(Trs):
    #computes the transpose of a transaction dataset
    #Author: Andre O. Falcao (c) 2020-2022
    res=[]
    for t in Trs: res+=t
    return set(res)

def getMinSupport(trs, min_support):
    #Gets the minimum support itemsets for a list of transactions (trs) given a min_support level
    #Author: Andre O. Falcao (c) 2020-2022
    N=len(trs)
    tr_sets=[set(tr) for tr in trs]
    supports={}
    all_items=getAllItems(tr_sets)
    transp=GetTranspose(trs)
    items=[]
    for it in all_items: 
        good_trans=transp[it]
        supp=len(good_trans)/N
        if supp>=min_support: 
            items.append(it)
    MinSupportSets(set(), min_support, set(items), transp, supports, N, None) #, set(range(N))
    return supports

def freqitemsets(trs, min_support):
    #Entry point - Gets the minimum support itemsets for a list of transactions given a min_support level
    #Returs a Pandas dataset for compatibility with mlxtend
    #Author: Andre O. Falcao (c) 2020-2022
    FI = getMinSupport(trs, min_support)
    #FI = Support(trs, min_support)
    D = {"support": list(FI.values()), "itemsets": list(FI.keys())}
    return pd.DataFrame(D)
