import re, os

from openpyxl import Workbook
"""
subcriber number
number state
subcriber status
additional status
"""
def check_Region() -> bool:
    pass

def clean(lt) -> tuple:

    for i in range(lt):
        if (lt[i][0] == "Call-in"):
            pass
def main(path) -> tuple:
    with open(path, 'r') as f:
        val = f.read()
        split_tag = "\n---    END\n\nLST MSBR:D=K"
        firL = val.split(split_tag)
        
        legths = [len(re.split('\n',i)) for i in firL]
        output = []
        for item  in (firL):
            secL = re.split('\n', item)
            if len(item) > min(legths):
                subNo, noSt, subSts, adSts = re.sub(' ','',secL[17]).split('=')[1], re.sub(' ','',secL[24]).split('=')[1], re.sub(' ','',secL[26]).split('=')[1], re.sub(' ','',secL[27]).split('=')[1]
                
                cOutai, cOut_counter = callOut(secL)

                cInAi, cIn_counter = callIn(secL, cOut_counter)
                
                #Still need to add cOutai and cInai
                
                output.append((subNo, noSt, subSts, adSts,cOutai, cInAi))
        return output

def callOut(secL):
    cOutAi = []
    cOut_counter = 0
    st_counter = 0
    for m in range(len(secL)):
        secL[m] = re.sub(' ','',secL[m])
        if "Call-outauthority" in secL[m]:
            st_counter = m
            break
        
    print(st_counter)
    for it in range(st_counter, 85):
        secL[it] = re.sub(' ','',secL[it])
        if "Call-inauthority" not in  secL[it]:
            cOutAi.append(secL[it].split("="))
        else:
            cOut_counter = it
            break
    print(cOut_counter)
    return cOutAi, cOut_counter

def callIn(secL, cIn_counter):
    cInAi = []
    for itj in range(cIn_counter, 129):
        secL[itj] = re.sub(' ','',secL[itj])
        if "Supplementaryservice" not in secL[itj]:
            cInAi.append(secL[itj].split("="))
        else:
            cIn_counter = itj
            break
    return cInAi, cIn_counter

def create_output(info_list, name):
        wb = Workbook()
        ws = wb.active
        
        ws.append(("Subscriber Number", "Number Status", "Subscriber Status", "Additional Status"))
        for i in info_list:
            ws.append(i)
        wb.save(os.path.join("outputs", name))

# create_output(all('inpt.txt'), 'Paro-AC-08.xlsx')
#TEST


print(main('inpt.xlsx'))