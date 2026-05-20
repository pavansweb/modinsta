import os
import re
import sys
import argparse

def apply_patch(target_root, patch_file):
    with open(patch_file, 'r') as f:
        content = f.read()

    # Split by file sections if multiple files are in one patch
    # Matches: ## File: `path/to/file` or **File:** `path/to/file`
    # Also handles bold colons and backticks variations
    sections = re.split(r'(?:## |\*\*)File:?\**[:\s]*[`*]*([^`*\s\(\)]+)[`*]*', content)

    if len(sections) < 3:
        print(f"  No file sections found in {patch_file}")
        return

    for i in range(1, len(sections), 2):
        rel_path = sections[i]
        section_content = sections[i+1]

        target_path = os.path.join(target_root, rel_path)
        if not os.path.exists(target_path):
            print(f"  Warning: Target file {target_path} not found. Skipping section.")
            continue

        # Extract Search/Replace blocks
        # Matches ### Search for: followed by ```smali ... ```
        search_blocks = re.findall(r'### Search for:\s*```smali\r?\n(.*?)\r?\n```', section_content, re.DOTALL)
        replace_blocks = re.findall(r'### Replace with:\s*```smali\r?\n(.*?)\r?\n```', section_content, re.DOTALL)

        # Matches ### Append to file: followed by ```smali ... ```
        append_blocks = re.findall(r'### Append to file:\s*```smali\r?\n(.*?)\r?\n```', section_content, re.DOTALL)

        with open(target_path, 'r') as f:
            file_data = f.read()

        new_data = file_data

        if search_blocks and replace_blocks:
            for s, r in zip(search_blocks, replace_blocks):
                if s in new_data:
                    new_data = new_data.replace(s, r)
                    print(f"  Applied replacement in {rel_path}")
                else:
                    # Try with normalized line endings if direct match fails
                    s_norm = s.replace('\r\n', '\n')
                    new_data_norm = new_data.replace('\r\n', '\n')
                    if s_norm in new_data_norm:
                         new_data = new_data_norm.replace(s_norm, r.replace('\r\n', '\n'))
                         print(f"  Applied replacement (normalized) in {rel_path}")
                    else:
                        print(f"  Warning: Search block not found in {rel_path}")
                        # Debug: print first line of search block
                        # print(f"  Search start: {s.splitlines()[0] if s.splitlines() else ''}")

        for a in append_blocks:
            if a not in new_data:
                new_data = new_data.rstrip() + "\n\n" + a + "\n"
                print(f"  Appended block to {rel_path}")
            else:
                print(f"  Block already exists in {rel_path}, skipping append.")

        if new_data != file_data:
            with open(target_path, 'w') as f:
                f.write(new_data)

def main():
    parser = argparse.ArgumentParser(description="Apply Smali patches from markdown files.")
    parser.add_argument("target_root", help="Root directory of the decompiled APK.")
    parser.add_argument("--patches_dir", default="patches", help="Directory containing .md patch files.")
    args = parser.parse_args()

    if not os.path.isdir(args.target_root):
        print(f"Error: {args.target_root} is not a directory.")
        sys.exit(1)

    if not os.path.isdir(args.patches_dir):
        print(f"Error: {args.patches_dir} is not a directory.")
        sys.exit(1)

    patch_files = [f for f in os.listdir(args.patches_dir) if f.endswith(".md")]
    if not patch_files:
        print(f"No .md files found in {args.patches_dir}")
        return

    for filename in sorted(patch_files):
        print(f"Processing {filename}...")
        apply_patch(args.target_root, os.path.join(args.patches_dir, filename))

if __name__ == "__main__":
    main()
