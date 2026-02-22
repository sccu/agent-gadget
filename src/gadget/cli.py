import argparse
import sys
import os
import shutil

def init_command(target_dir, force=False):
    """
    Handles the 'init' command to perform installation tasks.
    """
    print(f"Initializing gadget in '{target_dir}'...")
    
    src_skills_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "skills")
    target_skills_dir = os.path.join(target_dir, "skills")
    
    if not os.path.exists(src_skills_dir):
        print(f"Error: Source skills directory not found at {src_skills_dir}")
        sys.exit(1)
        
    existing_items = []
    if os.path.exists(target_skills_dir):
        for item in os.listdir(src_skills_dir):
            if os.path.exists(os.path.join(target_skills_dir, item)):
                existing_items.append(item)
                
    if existing_items:
        if not force:
            print("Error: The following skills already exist:")
            for item in existing_items:
                print(f"  - {item}")
            print("Use the -f or --force option to overwrite existing skills.")
            sys.exit(1)
        else:
            print("Force option provided. Removing existing skills...")
            for item in existing_items:
                tgt_path = os.path.join(target_skills_dir, item)
                if os.path.isdir(tgt_path):
                    shutil.rmtree(tgt_path)
                else:
                    os.remove(tgt_path)
                    
    try:
        shutil.copytree(src_skills_dir, target_skills_dir, dirs_exist_ok=True)
        print(f"Copied skills to {target_skills_dir}")
    except Exception as e:
        print(f"Failed to copy skills: {e}")
        sys.exit(1)
        
    print("Installation complete.")

def main():
    parser = argparse.ArgumentParser(description="Gadget CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # 'init' command definition
    init_parser = subparsers.add_parser("init", help="Perform installation")
    init_parser.add_argument("dir", nargs="?", default=".", help="Target directory for initialization (defaults to current directory)")
    init_parser.add_argument("-f", "--force", action="store_true", help="Force installation by overwriting existing items")
    
    args = parser.parse_args()
    
    if args.command == "init":
        init_command(args.dir, force=args.force)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
