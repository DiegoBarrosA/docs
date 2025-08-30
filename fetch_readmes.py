import os
import requests
import yaml

PROJECTS_DIR = "docs/projects"

def load_repos(config_file="repos.yaml"):
    with open(config_file, "r") as f:
        data = yaml.safe_load(f)
    return data["repos"]

def fetch_readme(owner_repo):
    owner, repo = owner_repo.split("/")
    # Intenta main primero, luego master
    for branch in ["main", "master"]:
        url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/README.md"
        r = requests.get(url)
        if r.status_code == 200:
            return r.text
    print(f"README.md no encontrado para {owner_repo}")
    return None

def save_readme(repo, content):
    repo_dir = os.path.join(PROJECTS_DIR, repo.split("/")[1])
    os.makedirs(repo_dir, exist_ok=True)
    index_path = os.path.join(repo_dir, "index.md")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    repos = load_repos()
    for repo in repos:
        print(f"Descargando README de {repo}...")
        content = fetch_readme(repo)
        if content:
            save_readme(repo, content)
            print(f"Guardado en projects/{repo.split('/')[1]}/index.md")
        else:
            print(f"Saltando {repo} (README no encontrado)")

if __name__ == "__main__":
    main()
