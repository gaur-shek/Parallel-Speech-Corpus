# importing libraries 
import speech_recognition as sr 
  
import os 
import glob
from pydub import AudioSegment 
from pydub.silence import split_on_silence 
import pandas as pd   

def STTI(csvpath, transPath, chunksDub, langCode):
    IsSR = {}
    indexCountSR = {}
    s = 0 
    for chunk in glob.glob(chunksDub + "*.*", recursive=True):        
        base=os.path.basename(chunk)
        kma, ex = os.path.splitext(base)
        result = ''.join([aa for aa in kma if aa.isdigit()])
        fh = open(transPath+kma+".txt", "w+", encoding = "utf-8")   
        
        file = chunk 
        
        r = sr.Recognizer() 
        try: 
             
            with sr.AudioFile(file) as source: 
                
                 
                audio_listened = r.listen(source) 
                rec = r.recognize_google(audio_listened, language= langCode ) 
                fh.write(rec+". ") 
                if rec == "":
                    
                    IsSR[int(result)] = "0"
                    indexCountSR[int(result)] = "0"
                    
                    os.remove(file)
                    fh.close()
                    os.remove(transPath+kma+".txt")
                    continue 
                base=os.path.basename(chunk)
                kma, ex = os.path.splitext(base)
                IsSR[int(result)] = "1"

                
        except:
            
            IsSR[int(result)] = "0"
            os.remove(file)
            fh.close()
            os.remove(transPath+kma+".txt")
            continue
    import collections
    izR = collections.OrderedDict(sorted(IsSR.items()))
    inzCou = collections.OrderedDict(sorted(indexCountSR.items()))
    izR2 = []
    inzCou2 = []
    for i in izR:
        izR2.append(izR[i])
    
    s = 0 
    for i in izR2:
        if i == "1":
            s = s + 1
            inzCou2.append(s)
        else:
            inzCou2.append("0")
    spath = pd.read_csv(csvpath)
    #print(len(IsSR))
    spath.insert(5,"Speech Recognition", izR2)
    spath.insert(6,"Index SR", inzCou2) # index SR for similarity 
    spath.to_csv(csvpath, index=False)

            
