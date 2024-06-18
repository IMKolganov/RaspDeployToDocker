import os
import subprocess

# Constants
CURRENT_DIR = os.getcwd() 
DEPLOY_FOLDER = 'deploy'
REPO_NAME = 'RaspDownloadPy'
REPO_PATH = os.path.join(CURRENT_DIR, DEPLOY_FOLDER, REPO_NAME)
REPO_URL = 'https://github.com/IMKolganov/RaspDownloadPy.git'

def clone_repository(repo_url, repo_path):
    """Clone the repository if the directory is empty or does not exist."""
    try:
        if not os.path.exists(repo_path) or not os.listdir(repo_path):
            subprocess.run(['git', 'clone', repo_url, repo_path], check=True)
            print(f"Repository cloned to {repo_path}")
        else:
            print(f"Directory {repo_path} is not empty. Skipping cloning.")
    except Exception as e:
        print(f"Error cloning repository: {e}")

def check_git_changes(repo_path, target_branch):
    """Check for changes in the Git repository on the specified branch."""
    try:
        os.chdir(repo_path)  # Change to the repository directory

        # Update the local repository
        subprocess.run(['git', 'pull', 'origin', target_branch], check=True)

        # Checkout the target branch
        subprocess.run(['git', 'checkout', target_branch], check=True)

        # Check the status of the repository
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"Error executing git command: {result.stderr}")
            return False

        if result.stdout.strip():
            return True  # Changes detected
        else:
            return False  # No changes

    except Exception as e:
        print(f"Error checking Git changes: {e}")
        return False
    
def build_and_run_docker():
    """Build Docker image and run container."""
    try:
        # Navigate to the directory containing Dockerfile
        docker_directory = os.path.join(REPO_PATH, 'path', 'to', 'dockerfile')  # Specify path to Dockerfile
        os.chdir(docker_directory)

        # Build Docker image
        build_command = ['docker', 'build', '-t', 'rasp_app', '.']
        build_process = subprocess.run(build_command, check=True, capture_output=True, text=True)
        print("Docker build output:", build_process.stdout)

        # Run Docker container
        run_command = ['docker', 'run', '--rm', '-d', '-p', '5000:5000', 'rasp_app']
        run_process = subprocess.run(run_command, check=True, capture_output=True, text=True)
        print("Docker run output:", run_process.stdout)

        print("Application successfully deployed in Docker container.")

    except subprocess.CalledProcessError as e:
        print(f"Error running subprocess command: {e}")
        if e.output:
            print("Subprocess output:", e.output)
    except Exception as e:
        print(f"Error building and running Docker container: {e}")


if __name__ == "__main__":
    clone_repository(REPO_URL, REPO_PATH)

    if check_git_changes(REPO_PATH, 'main'):
        print("There are changes in the 'main' branch of the Git repository.")
        build_and_run_docker()
    else:
        print("No changes in the 'main' branch of the Git repository.")