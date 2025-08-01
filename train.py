import os
from azure.ai.ml import MLClient, Environment, ComputeTarget, ComputeSchedule, Job, PythonScriptWorker
from azure.ai.ml.train.run import Run

# Replace with your Azure Machine Learning workspace and compute details
workspace_name = "<your_workspace_name>"
compute_name = "<your_compute_instance_name>"
environment_name = "<your_environment_name>"  # e.g., "my-gpu-env"
job_name = "gpu-example-job"
run_name = "gpu-run-1"
output_path = "https://<your_workspace_name>.blob.core.windows.net/runs/" + run_name

# Initialize the ML client
ml_client = MLClient(workspace_name)

# 1. Get the environment
environment = ml_client.environments.get(name=environment_name)

# 2. Get the compute target (GPU)
compute_target = ComputeTarget.get(workspace_name, name=compute_name)

# 3. Create a Python environment
python_env = Environment(compute=compute_target, environment=environment)

# 4. Create a job
job = Job(compute=python_env, name=job_name)

# 5. Define the script (replace with your actual script)
script_content = """
import torch

def train_model():
    print("Training on GPU...")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = torch.nn.Linear(10, 1)  # Example model
    optimizer = torch.optim.Adam(model.parameters())
    loss_fn = torch.nn.MSELoss()

    # Dummy data
    x = torch.randn(100, 10)
    y = torch.randn(100, 1)

    for epoch in range(10):
        optimizer.zero_grad()
        output = model(x)
        loss = loss_fn(output, y)
        loss.backward()
        optimizer.step()
        print(f"Epoch {epoch+1}, Loss: {loss.item()}")

if __name__ == "__main__":
    train_model()
"""

# 6. Create the run
run = Run(job_id=job.id, name=run_name, script_content=script_content, environment=environment)

# 7. Start the run
run.start()

print(f"Run started: {run.id}")
