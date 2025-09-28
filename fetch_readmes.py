import os
import re
import requests
import yaml
from urllib.parse import urlparse
import base64
import json

PROJECTS_DIR = "projects"

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

def get_github_api_tree(owner_repo, branch="main"):
    """Fetch the GitHub repository tree to check for docs directory structure"""
    owner, repo = owner_repo.split("/")
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    return None

def fetch_docs_directory(owner_repo, branch="main"):
    """Fetch all files from the /docs directory of a repository"""
    tree_data = get_github_api_tree(owner_repo, branch)
    if not tree_data:
        return None
    
    docs_files = []
    for item in tree_data.get('tree', []):
        if item['path'].startswith('docs/') and item['type'] == 'blob':
            docs_files.append(item['path'])
    
    if not docs_files:
        return None
    
    owner, repo = owner_repo.split("/")
    fetched_docs = {}
    
    for file_path in docs_files:
        url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{file_path}"
        r = requests.get(url)
        if r.status_code == 200:
            # Store relative path within docs directory
            relative_path = file_path[5:]  # Remove 'docs/' prefix
            fetched_docs[relative_path] = r.text
    
    return fetched_docs if fetched_docs else None

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

def save_docs_structure(repo, docs_files):
    """Save the entire docs directory structure for a repository"""
    repo_name = repo.split("/")[1]
    repo_dir = os.path.join(PROJECTS_DIR, repo_name)
    os.makedirs(repo_dir, exist_ok=True)
    
    # Create a docs subdirectory within the project
    docs_dir = os.path.join(repo_dir, "docs")
    os.makedirs(docs_dir, exist_ok=True)
    
    for relative_path, content in docs_files.items():
        file_path = os.path.join(docs_dir, relative_path)
        # Create subdirectories if needed
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"Guardado: {file_path}")
    
    # Create an index.md that references the docs structure
    index_content = f"""---
layout: default
title: "{repo_name} Documentation"
---

# {repo_name} Documentation

Esta página contiene la documentación completa del proyecto {repo_name}.

## Estructura de Documentación

"""
    
    # Add links to main documentation files
    for relative_path in sorted(docs_files.keys()):
        if relative_path.endswith('.md'):
            title = os.path.splitext(os.path.basename(relative_path))[0].replace('-', ' ').title()
            link_path = f"docs/{relative_path}"
            index_content += f"- [{title}]({link_path})\n"
    
    index_path = os.path.join(repo_dir, "index.md")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_content)

def main():
    repos = load_repos()
    for repo in repos:
        print(f"Procesando repositorio {repo}...")
        
        # First, try to fetch the full docs directory
        for branch in ["main", "master"]:
            docs_files = fetch_docs_directory(repo, branch)
            if docs_files:
                print(f"Encontrado directorio /docs en {repo} (rama {branch})")
                # Process images for each docs file
                repo_dir = os.path.join(PROJECTS_DIR, repo.split("/")[1])
                processed_docs = {}
                for relative_path, content in docs_files.items():
                    if relative_path.endswith('.md'):
                        content = process_images(content, repo, branch, repo_dir)
                    processed_docs[relative_path] = content
                
                save_docs_structure(repo, processed_docs)
                print(f"Documentación completa guardada en projects/{repo.split('/')[1]}/")
                break
        else:
            # Fallback to README if no docs directory found
            print(f"No se encontró directorio /docs, buscando README...")
            md_content, branch = fetch_readme(repo)
            if md_content:
                repo_dir = os.path.join(PROJECTS_DIR, repo.split("/")[1])
                md_content = process_images(md_content, repo, branch, repo_dir)
                save_readme(repo, md_content)
                print(f"README guardado en projects/{repo.split('/')[1]}/index.md")
            else:
                print(f"Saltando {repo} (ni docs ni README encontrados)")

if __name__ == "__main__":
    main()
