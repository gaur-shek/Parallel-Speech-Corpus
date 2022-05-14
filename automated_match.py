import pandas as pd 




def matchSegments(encsv, hicsv, csvresult, txtsim): # two csv files tr ar return csv file for both 
    sumDurationHI = 0
    sumDurationEN = 0
    sumSegmentsHI  = 0
    sumSegmentsEN = 0 
    LstIndHI = []
    LstDuHI = []
    LststrtHI = []
    LststpHI = []
    LstlabHI = []
    LstIndEN = []
    LstDuEN = []
    LststrtEN = []
    LststpEN = []
    LstlabEN = []
    LstSim = [] 
    array2D = []
    param = [2,3]
    en = pd.read_csv(encsv)
    hi = pd.read_csv(hicsv)
    res = open(csvresult,"w+")
    res.write("0")
    res.close()
    res = pd.read_csv(csvresult) 
    with open(txtsim, 'r') as f:
        for line in f.readlines():
            array2D.append(line.split(' '))

    l1 = dict()

    i = 0


    x = len(en)
    y = len(hi)
    i = 0
    j = 0
    while i < x-1:
        j = 0
        while j < y:
            #j = i 
            if abs(int(en['start'][i])-int(hi['start'][j])) <= param[1] and  abs(int(en['Duration'][i])-int(hi['Duration'][j])) <= param[0] and en['labels'][i] == hi['labels'][j] and hi['Speech Recognition'][j] == 1 and en['Speech Recognition'][i] == 1: 
                if int(en['Index1'][i]) not in l1 and int(hi['Index1'][j]) not in l1.values():
                    
                    l1[en['Index1'][i]]= hi['Index1'][j]
                    X = int(en['Index1'][i])
                    Y = int(hi['Index1'][j])
                    LstIndHI.append(Y)
                    LstIndEN.append(X)
                    LststrtHI.append(hi['start'][j])
                    LststrtEN.append(en['start'][i])
                    LststpHI.append(hi['stop'][j])
                    LststpEN.append(en['stop'][i])
                    sumDurationHI = sumDurationHI + int(hi['Duration'][j])
                    sumDurationEN = sumDurationEN + int(en['Duration'][i])
                    LstDuHI.append(hi['Duration'][j])
                    LstDuEN.append(en['Duration'][i])
                    LstlabHI.append(hi['labels'][j])
                    LstlabEN.append(en['labels'][i])
                    RX = int(en['Index SR'][i])
                    RY = int(hi['Index SR'][j])
                    LstSim.append(array2D[RX-1][RY-1])
                    sumSegmentsHI = sumSegmentsHI + 1
                    sumSegmentsEN = sumSegmentsEN+ 1
                    #l1[X]= Y
                    #print(X+ " "+ Y)
                    
                    
                
            j = j + 1 
        i = i + 1
        
    # 'start' with list of chunks no need for label
    # later step remove from dictionary same values 
    # create three dictionaries 1 for both 1 for en vs. hi 1 for hi vs. en
    # last step apply the filtration process which is if less < 2 secs and Index1in SR krmal 2D array 
    #similarity remve if less than <.45
    # remove speaker diarization
    print("---------------------------------------------------")

    i = 0
    j = 0
    du = [] 
    ch = []
    end = []
    l2 = dict()
    try:
        while i < x - 1: 
            j = 0
            z = 0
            du = []
            ch = []
            end = [] # end 
            strt = []
            lab = [] # label 
            simPr = []
            indSR = []
            while j < y:
				#j = i 
                if abs(int(en['start'][i])-int(hi['start'][j])) <= param[1] and int(en['stop'][i]) > int(hi['stop'][j]) and en['labels'][i] == hi['labels'][j] and hi['Speech Recognition'][j] == 1 and en['Speech Recognition'][i] == 1: 
                    print("passeD")
                    du.append(int(hi['Duration'][j]))
                    ch.append(str(hi['Index1'][j]))
                    end.append(str(hi['stop'][j]))
                    strt.append(str(hi['start'][j]))
                    lab.append(str(hi['labels'][j]))                
                    indSR.append(str(hi['Index SR'][j]))
                    z = j 
                    j = j + 1 
                    continue 
                elif z != 0 and abs(int(hi['stop'][z]) - int(hi['start'][j])) <= 1 and int(en['stop'][i]) > int(hi['stop'][j]) and hi['labels'][j] != 'noEnergy' and hi['Speech Recognition'][j] == 1 and en['Speech Recognition'][i] == 1: 
					
                    du.append(int(hi['Duration'][j]))
                    ch.append(str(hi['Index1'][j]))
                    end.append(str(hi['stop'][j]))
                    strt.append(str(hi['start'][j]))
                    lab.append(str(hi['labels'][j]))                
                    indSR.append(str(hi['Index SR'][j]))
                    z = j 
                    j = j + 1 
                    continue 
                elif z!= 0 and abs(int(hi['stop'][z]) - int(hi['start'][j])) <= 1 and abs(int(en['stop'][i]) - int(hi['stop'][j])) <= 2 and hi['labels'][j] != 'noEnergy' and hi['Speech Recognition'][j] == 1 and en['Speech Recognition'][i] == 1: 
					#print("passeD")
                    du.append(int(hi['Duration'][j]))
                    ch.append(str(hi['Index1'][j]))
                    end.append(str(hi['stop'][j]))
                    strt.append(str(hi['start'][j]))
                    lab.append(str(hi['labels'][j]))                
                    indSR.append(str(hi['Index SR'][j]))
                    bb = True 
                    if int(en['Index1']	[i]) not in l2 and int(en['Index1'][i]) not in l1 and int(hi['Index1'][j]) not in l2.values() and abs(sum(du)-int(en['Duration'][i])) <= param[0]:
                        s = ';'.join(ch)
                        es = ';'.join(end)
                        rt = ';'.join(strt)
                        lb = ';'.join(lab)
                        du2 = []
                        sumDurationHI = sumDurationHI + sum(du)
                        sumDurationEN = sumDurationEN + int(en['Duration'][i])
                        sumSegmentsEN = sumSegmentsEN + 1
                        for kz in du:
                            du2.append(str(kz))
                            sumSegmentsHI = sumSegmentsHI + 1
                        drt = ';'.join(du2)
                        
                        inS = ';'.join(indSR)
                        
                        for zzz in ch:
                            if zzz in l1: 
                                bb = False  
                        if bb == False:
                            break
                        l2[en['Index1'][i]]= s
						#l1[X]= Y
                        X = int(en['Index1'][i])
                        LstIndHI.append(s)
                        LstIndEN.append(X)
                        LststrtHI.append(rt)
                        LststrtEN.append(en['start'][i])
                        LststpHI.append(es)
                        LststpEN.append(en['stop'][i])
                        LstDuHI.append(drt)
                        LstDuEN.append(en['Duration'][i])
                        LstlabHI.append(lb)
                        LstlabEN.append(en['labels'][i])
                        RX = int(en['Index SR'][i])
                        for k in indSR:
                            zi = int(k)
                            simPr.append(str(array2D[RX-1][zi-1]))
                        ziD = ';'.join(simPr)
                        LstSim.append(ziD)
						#Y = str(ar['Index1'][j])
						#l1[X]= Y
						#print(X + " " + s)
						#print(s)
				
					
                j = j + 1 
            i = i + 1
    except:
        print("error")
       
    i = 0
    j = 0
    du = [] 
    ch = []
    end = []
    l2_hi_en = dict()
    print("---------------------------------------------------")
    while j < y: 
        i = 0
        z = 0
        du = []
        ch = []
        end = [] # end 
        strt = []
        lab = [] # label 
        simPr = []
        indSR = []
        
        while i < x -1:
            #j = i 
            if abs(en['start'][i].astype(int)-int(hi['start'][j])) <= param[1] and en['stop'][i].astype(int) < int(hi['stop'][j]) and en['labels'][i] == hi['labels'][j] and hi['Speech Recognition'][j] == 1 and en['Speech Recognition'][i] == 1: 
                du.append(int(en['Duration'][i]))
                ch.append(str(en['Index1'][i]))
                end.append(str(en['stop'][i]))
                strt.append(str(en['start'][i]))
                lab.append(str(en['labels'][i]))
                indSR.append(str(en['Index SR'][i]))
                
                z = i 
                i = i + 1
                continue 
            elif z != 0 and abs(en['stop'][z].astype(int) - en['start'][i].astype(int)) <= 1 and en['stop'][i].astype(int) < int(hi['stop'][j]) and en['labels'][i] != 'noEnergy' and hi['Speech Recognition'][j] == 1 and en['Speech Recognition'][i] == 1: 
                du.append(int(en['Duration'][i]))
                ch.append(str(en['Index1'][i]))
                end.append(str(en['stop'][i]))
                strt.append(str(en['start'][i]))
                lab.append(str(en['labels'][i]))
                indSR.append(str(en['Index SR'][i]))
                z = i 
                i = i + 1
                continue 
            elif z!= 0 and abs(en['stop'][z].astype(int) - en['start'][i].astype(int)) <= 1 and abs(en['stop'][i].astype(int) - int(hi['stop'][j]))<=2 and en['labels'][i] != 'noEnergy' and hi['Speech Recognition'][j] == 1 and en['Speech Recognition'][i] == 1: 
                du.append(int(en['Duration'][i]))
                ch.append(str(en['Index1'][i]))
                end.append(str(en['stop'][i]))
                strt.append(str(en['start'][i]))
                lab.append(str(en['labels'][i]))
                indSR.append(str(en['Index SR'][i]))
                bb = True 
                if hi['Index1'][j].astype(int) not in l2_hi_en and int(hi['Index1'][j]) not in l1 and int(en['Index1'][i]) not in l2_hi_en.values() and abs(sum(du)-int(hi['Duration'][j])) <= param[0]:
                    s = ';'.join(ch)
                    es = ';'.join(end)
                    rt = ';'.join(strt)
                    lb = ';'.join(lab)
                    du2 = []
                    sumDurationHI = sumDurationHI + int(hi['Duration'][j])
                    sumDurationEN = sumDurationEN + sum(du)
                    sumSegmentsHI = sumSegmentsHI + 1
                    for kz in du:
                       du2.append(str(kz))
                       sumSegmentsEN = sumSegmentsEN + 1
                    drt = ';'.join(du2)
                    inS = ';'.join(indSR)
                    for zzz in ch:
                        if zzz in l1: 
                          bb = False  
                    if bb == False:
                        break
                    l2_hi_en[ar['Index1'][j]]= s
                    #l1[X]= Y
                    X = int(hi['Index1'][j])
                    LstIndHI.append(X)
                    LstIndEN.append(s)
                    LststrtHI.append(hi['start'][j])
                    LststrtEN.append(rt)
                    LststpHI.append(hi['stop'][j])
                    LststpEN.append(es)
                    LstDuHI.append(hi['Duration'][j])
                    LstDuEN.append(drt)
                    LstlabHI.append(hi['labels'][j])
                    LstlabEN.append(lab)
                    RX = int(hi['Index SR'][j])
                    for k in indSR:
                        zi = int(k)
                        simPr.append(str(array2D[zi-1][RX-1]))   
                    ziD = ';'.join(simPr)
                    LstSim.append(ziD)
                    

                
            i = i + 1 
        j = j + 1   
    res.insert(1, "Dub", LstIndHI )
    res.insert(2, "startDub", LststrtHI )
    res.insert(3, "stopDub", LststpHI )
    res.insert(4, "DurationDub", LstDuHI )
    res.insert(5, "labelDub", LstlabHI )
    res.insert(6, "Org", LstIndEN )
    res.insert(7, "startOrg",LststrtEN  )
    res.insert(8, "stopOrg", LststpEN )
    res.insert(9, "DurationOrg", LstDuEN )
    res.insert(10, "labelOrg",LstlabEN )
    res.insert(11, "Similarity",LstSim )
    sumDuHI = 0
    sumDuEN = 0
    
    res.to_csv(csvresult, index= False)
    
    
