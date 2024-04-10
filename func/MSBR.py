import re


def main(path) -> list:
    with open(path, 'r') as file:
        val = file.read()
        
        all_no = val.split('LST MSBR:D=K')

        return get_details(all_no)[0]
        

def get_details(all_no) -> list:
    det = [re.sub(' ','',no).split('\n') for no in all_no]
    
    out_det = []
    for dt in det:
        if len(dt)>1 and len(dt) < 140:
            try:
                c_Out = call_out(dt)[1]
                c_In = call_in(dt, c_Out)[1]
                subNo, subSts, adSts, cOut, cIn, supSer = dt[17].removeprefix("Subscribernumber="),dt[26].removeprefix("Subscriberstatus="),dt[27].removeprefix("Additionalstatus="), "\n".join(call_out(dt)[0]), "\n".join(call_in(dt,c_Out)[0]), dt[c_In]
                

                out_det.append((subNo, subSts, adSts, cOut, cIn, supSer))
            except IndexError:
                out_det.append((0,0,0))

    
    return out_det,det

    # for i, it in enumerate(det):
    #     print(i,it)
    
def call_out(dt) -> list:
    c_Out = []
    cOut = 0
    st = 0
    for i in range(27, 65):
        if "Call-outauthority" in dt[i]:
            break
        else:
            st = i
    for i in range(st+1, 100):
        if "Call-inauthority" in dt[i]:
            cOut = i
            break
        else:
            c_Out.append(dt[i])
            cOut = i
    return c_Out, cOut

def call_in(dt, cOut):
    c_In = []
    cIn = cOut
    for i in range(cOut, cOut+100):
        try:
            if "Supplementaryservice" in dt[i]:
                cIn = i
                break
            else:
                c_In.append(dt[i])
                cIn = i
        except IndexError:
            c_In.append("NULL")

    return c_In, cIn