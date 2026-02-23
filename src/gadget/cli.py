import argparse
import sys
import os
import shutil
from typing import List

def get_existing_items(src_dir: str, target_dir: str) -> List[str]:
    """타겟 디렉토리에 이미 존재하는 항목 목록을 반환"""
    if not os.path.exists(target_dir):
        return []
    
    src_items = set(os.listdir(src_dir))
    target_items = set(os.listdir(target_dir))
    return list(src_items.intersection(target_items))

def remove_items(target_dir: str, items: List[str]) -> None:
    """타겟 디렉토리 내 특정 항목들을 안전하게 삭제"""
    errors = []
    for item in items:
        tgt_path = os.path.join(target_dir, item)
        try:
            if os.path.isdir(tgt_path):
                shutil.rmtree(tgt_path)
            else:
                os.remove(tgt_path)
        except OSError as e:
            errors.append(f"Failed to remove {tgt_path}: {e}")
            
    if errors:
        for err in errors:
            print(f"Error: {err}")
        sys.exit(1)

def install_items(src_dir: str, target_dir: str, force: bool, item_type: str) -> None:
    """항목 설치 로직"""
    if not os.path.exists(src_dir):
        print(f"Warning: Source {item_type} directory not found at {src_dir}. Skipping...")
        return

    existing_items = get_existing_items(src_dir, target_dir)
    
    if existing_items:
        if not force:
            print(f"Error: The following {item_type} already exist:")
            for item in existing_items:
                print(f"  - {item}")
            print(f"Use the -f or --force option to overwrite existing {item_type}.")
            sys.exit(1)
        
        print(f"Force option provided. Removing existing {item_type}...")
        remove_items(target_dir, existing_items)
            
    try:
        shutil.copytree(src_dir, target_dir, dirs_exist_ok=True)
        # Gather directory names that were successfully copied
        copied_items = [item for item in os.listdir(src_dir) if os.path.exists(os.path.join(target_dir, item))]
        print(f"Successfully installed {item_type}:")
        for item in copied_items:
            print(f"  - {item}")
    except Exception as e:
        print(f"Error: Failed to copy {item_type}: {e}")
        sys.exit(1)

def init_command(target_dir: str, force: bool = False) -> None:
    """
    Handles the 'init' command to perform installation tasks.
    """
    print(f"Initializing gadget in '{target_dir}'...")
    base_src_dir = os.path.dirname(__file__)
    base_target_dir = os.path.join(target_dir, ".agents")
    
    directories_to_install = ["skills", "workflows"]
    
    for dir_name in directories_to_install:
        src_dir = os.path.join(base_src_dir, dir_name)
        tgt_dir = os.path.join(base_target_dir, dir_name)
        install_items(src_dir, tgt_dir, force, dir_name)
        
    print("Installation complete.")

def main() -> None:
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
