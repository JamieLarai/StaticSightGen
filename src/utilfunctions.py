import os
import shutil
import logging

from markdownfuncs import extract_title, markdown_to_html_node

def copy_directory(src, dst):
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    # Delete all contents of the destination directory
    if os.path.exists(dst):
        shutil.rmtree(dst)
        logging.info(f"Deleted existing contents of {dst}")
    
    # Copy all contents from source to destination
    shutil.copytree(src, dst)
    logging.info(f"Copied contents from {src} to {dst}")
    
def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read markdown content
    with open(from_path, 'r') as f:
        markdown_content = f.read()
    
    # Read template content
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    # Extract title
    title = extract_title(markdown_content)
    
    # Replace placeholders in template
    full_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    
    # Replace href="/" and src="/" with basepath
    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')
    
    # Ensure destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # Write full HTML to destination path
    with open(dest_path, 'w') as f:
        f.write(full_html)
        
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        if os.path.isdir(item_path):
            # Recursively generate pages for subdirectories
            # Calculate the corresponding destination subdirectory
            relative_dir = os.path.relpath(item_path, dir_path_content)
            dest_subdir = os.path.join(dest_dir_path, relative_dir)
            generate_pages_recursive(item_path, template_path, dest_subdir, basepath)
        elif item.endswith(".md"):
            # Generate page for markdown file
            relative_path = os.path.relpath(item_path, dir_path_content)
            dest_path = os.path.join(dest_dir_path, relative_path.replace(".md", ".html"))
            generate_page(item_path, template_path, dest_path, basepath)