from globus_compute_sdk import Executor
from pprint import pprint


# First, define the function ...
def submit_job():
    import subprocess
    import time
    output = None
    # submit a new job to slurm
    output = subprocess.run(["torchrun", "--nproc_per_node", "1", 
                             "/home/zyliang/llama-test/llama/example.py",
                             "--ckpt_dir", "/nfs/turbo/umms-dinov/LLaMA/1.0.1/llama/modeltoken/7B",
                             "--tokenizer_path", "/nfs/turbo/umms-dinov/LLaMA/1.0.1/llama/modeltoken/tokenizer.model"],
                            capture_output=True)
    if output.stderr is None:
        return output.stdout.decode()
    else:
        return output.stderr.decode()


test_endpoint_id = '03d80c2e-f629-497a-a38c-85819e5f3209'
# ... then create the executor, ...
with Executor(endpoint_id=test_endpoint_id) as gce:
    # ... then submit for execution, ...
    future = gce.submit(submit_job)
    print("\nSubmitted the function to Globus endpoint.\n")
    # ... and finally, wait for the result
    # print(future.result())
    with open("debug/output.txt", "w") as out:
        out.write(future.result())
