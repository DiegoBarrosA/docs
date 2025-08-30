docs/fetch_readmes.py
```
```python
import os
import re
import requests
import yaml
from urllib.parse import urlparse

PROJECTS_DIR = "docs/projects"

def load_repos(config_file="repos.yaml"):
    with open(config_file, "r") as f:
        data = yaml.safe_load(f)
    return data["repos"]

def fetch_readme(owner_repo):
    owner, repo = owner_repo.split("/")
    for branch in ["main", "master"]:
        url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/README.md"
        r = requests.get(url)
        if r.status_code == 200:
            return r.text, branch
    print(f"README.md no encontrado para {owner_repo}")
    return None, None

def fetch_and_save_image(img_url, save_dir, repo, branch):
    # Si la imagen es relativa, construye la URL cruda de GitHub
    if not img_url.startswith("http"):
        img_url = img_url.lstrip("./")
        owner, repo_name = repo.split("/")
        img_url = f"https://raw.githubusercontent.com/{owner}/{repo_name}/{branch}/{img_url}"
    parsed = urlparse(img_url)
    filename = os.path.basename(parsed.path)
    save_path = os.path.join(save_dir, filename)
    try:
        r = requests.get(img_url)
        if r.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(r.content)
            return save_path
        else:
            print(f"No se pudo descargar imagen: {img_url}")
    except Exception as e:
        print(f"Error descargando {img_url}: {e}")
    return None

def process_images(md_content, repo, branch, project_dir):
    # Encuentra imágenes Markdown ![alt](url)
    img_pattern = r'!\[.*?\]\((.*?)\)'
    # Encuentra imágenes HTML <img src="url">
    html_img_pattern = r'<img\s+[^>]*src=["\']([^"\']+)["\']'
    all_imgs = re.findall(img_pattern, md_content) + re.findall(html_img_pattern, md_content)
    assets_dir = os.path.join(project_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    replacements = {}
    for img_url in all_imgs:
        # No descargar imágenes externas que no sean de GitHub
        if img_url.startswith("http") and "githubusercontent.com" not in img_url and "github.com" not in img_url:
            continue
        local_path = fetch_and_save_image(img_url, assets_dir, repo, branch)
        if local_path:
            rel_path = os.path.relpath(local_path, project_dir)
            replacements[img_url] = rel_path.replace("\\", "/")
    # Reemplaza las rutas en el markdown
    for old, new in replacements.items():
        md_content = md_content.replace(f"({old})", f"({new})")
        md_content = md_content.replace(f'src="{old}"', f'src="{new}"')
    return md_content

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
        md_content, branch = fetch_readme(repo)
        if md_content:
            repo_dir = os.path.join(PROJECTS_DIR, repo.split("/")[1])
            md_content = process_images(md_content, repo, branch, repo_dir)
            save_readme(repo, md_content)
            print(f"Guardado en projects/{repo.split('/')[1]}/index.md (con imágenes locales)")
        else:
            print(f"Saltando {repo} (README no encontrado)")

if __name__ == "__main__":
    main()
