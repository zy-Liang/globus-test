from globus_compute_sdk import Executor
from pprint import pprint
import argparse


# First, define the function ...
def submit_job(prompt:str):
    import subprocess
    # run llama with torch
    output = subprocess.run(["torchrun", "--nproc_per_node", "1", 
                             "/home/zyliang/llama-test/llama/run.py", "--prompt", prompt,
                             "--ckpt_dir", "/nfs/turbo/umms-dinov/LLaMA/1.0.1/llama/modeltoken/7B",
                             "--tokenizer_path", "/nfs/turbo/umms-dinov/LLaMA/1.0.1/llama/modeltoken/tokenizer.model"],
                            capture_output=True)
    if output.returncode == 0:
        return output.stdout.decode()
    else:
        return output.stderr.decode()


test_endpoint_id = 'b9d9099c-4aed-499c-a020-743041a15521'

parser = argparse.ArgumentParser()
parser.add_argument("--prompt", type=str)
args = parser.parse_args()
prompt = args.prompt
if prompt is None:
    prompt = "The capital of France is"
# ... then create the executor, ...
with Executor(endpoint_id=test_endpoint_id) as gce:
    # ... then submit for execution, ...
    future = gce.submit(submit_job, prompt)
    print("\nSubmitted the function to Globus endpoint.\n")
    # ... and finally, wait for the result
    # print(future.result())
    with open("debug/output.txt", "w") as out:
        out.write(future.result())
