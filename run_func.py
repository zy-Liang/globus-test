from globus_compute_sdk import Executor
from pprint import pprint


# First, define the function ...
def submit_job():
    import subprocess
    import time
    # submit a new job to slurm
    job_script = "/home/zyliang/ondemand/data/sys/myjobs/projects/default/9/main_job.sh"
    account = "zyliang"
    output = subprocess.check_output(["sbatch", job_script]).decode()
    output = output.strip()
    # get the job id of the submitted job
    job_id = [ int(i) for i in output.split() if i.isdigit() ]
    job_id = job_id[0]
    time_interval = 5
    # iteratively check if the submitted job is completed
    while True:
        time.sleep(time_interval)
        output = subprocess.check_output(["squeue", "-u", account]).decode()
        output = output.strip()
        if not str(job_id) in output:
            break
    # read and print the output of slurm
    with open(f"slurm-{job_id}.out", "r") as output_file:
        output = output_file.read()
        return output


test_endpoint_id = '53d7e6d2-2e37-4991-91c5-e8a37009e811'
# ... then create the executor, ...
with Executor(endpoint_id=test_endpoint_id) as gce:
    # ... then submit for execution, ...
    future = gce.submit(submit_job)
    print("\nSubmitted the function to Globus endpoint.\n")
    # ... and finally, wait for the result
    print(future.result())
