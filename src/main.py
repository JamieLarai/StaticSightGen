from textnode import *
from utilfunctions import copy_directory, generate_pages_recursive
from markdownfuncs import markdown_to_html_node, extract_title
import os
import sys

def main(): 
    # Get the basepath from command line argument, default to "/"
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    
    # Get the base directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Define source and destination directories
    src_path = os.path.join(base_dir, "static")
    dst_path = os.path.join(base_dir, "docs")
    
    # Copy static files to docs directory
    copy_directory(src_path, dst_path)
    print("Static files copied to docs/")
    
    # Generate HTML pages from all markdown files in content directory
    content_dir = os.path.join(base_dir, "content")
    template_file = os.path.join(base_dir, "template.html")
    
    generate_pages_recursive(content_dir, template_file, dst_path, basepath)
    
    print("Site generation complete!")
    
    
if __name__ == "__main__":
    main()