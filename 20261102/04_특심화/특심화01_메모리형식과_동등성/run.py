from pathlib import Path
import torch
from tasks import channels_last_copy, compare_layouts
from support import seed_all,small_model,save_json

def main():
    seed_all();x=torch.rand(4,3,32,32);model=small_model()
    converted=channels_last_copy(x);report=compare_layouts(model,x)
    report.update(shape=list(converted.shape),stride=list(converted.stride()),same_values=torch.equal(x,converted),
                  distinct_storage=x.data_ptr()!=converted.data_ptr(),channels_last=converted.is_contiguous(memory_format=torch.channels_last))
    assert max(report[k] for k in ['output_max_abs','input_grad_max_abs','parameter_grad_max_abs'])<1e-5
    save_json('memory_contract.json',report)
    print('NCHW:',report['shape'],'stride:',report['stride'])
    print('값/독립 storage/출력·gradient 동등성 확인. 속도 이득은 별도 측정한다.')
if __name__=='__main__': main()
