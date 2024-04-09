from func.VSBR import main as vsbr
from func.MSBR import main as msbr
from func.output import create_output
#print(main('./uploads/vsbr_sample.txt'))
create_output(msbr('./uploads/inpt.txt'), 'inpt.xlsx')