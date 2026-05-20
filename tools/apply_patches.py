import os
import re
import sys
import argparse

def apply_patch(target_root, patch_file):
    with open(patch_file, 'r') as f:
        content = f.read()

    # Robust regex for file headers
    # Matches: ## File: `path`, **File:** `path`, etc.
    header_pattern = re.compile(r'(?mi)^[ \t]*(?:## |\*\*)File:?.*?\`([^`]+)\`')

    matches = list(header_pattern.finditer(content))

    if not matches:
        print(f"  No file sections found in {patch_file}")
        return

    for i, match in enumerate(matches):
        rel_path = match.group(1).strip()
        # The content of the section starts after the header
        start = match.end()
        end = matches[i+1].start() if i+1 < len(matches) else len(content)
        section_content = content[start:end]

        target_path = os.path.join(target_root, rel_path)
        if not os.path.exists(target_path):
            print(f"  Warning: Target file {target_path} not found. Skipping section {rel_path}.")
            continue

        # Extraction of Smali blocks
        search_blocks = re.findall(r'### Search for:\s*```smali\r?\n(.*?)\r?\n```', section_content, re.DOTALL)
        replace_blocks = re.findall(r'### Replace with:\s*```smali\r?\n(.*?)\r?\n```', section_content, re.DOTALL)
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
                    s_norm = s.replace('\r\n', '\n')
                    r_norm = r.replace('\r\n', '\n')
                    new_data_norm = new_data.replace('\r\n', '\n')
                    if s_norm in new_data_norm:
                         new_data = new_data_norm.replace(s_norm, r_norm)
                         print(f"  Applied replacement (normalized) in {rel_path}")
                    else:
                        print(f"  Warning: Search block not found in {rel_path}")

        for a in append_blocks:
            a_norm = a.replace('\r\n', '\n')
            new_data_norm = new_data.replace('\r\n', '\n')
            if a_norm not in new_data_norm:
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
    parser.add_argument("--patches_dir", default="patches", help="Directory containing .md patch files or a single .md file.")
    args = parser.parse_args()

    target_root = os.path.abspath(args.target_root)
    patches_path = os.path.abspath(args.patches_dir)

    if not os.path.isdir(target_root):
        print(f"Error: {target_root} is not a directory.")
        sys.exit(1)

    if os.path.isfile(patches_path):
        patch_files = [os.path.basename(patches_path)]
        patches_dir = os.path.dirname(patches_path)
    elif os.path.isdir(patches_path):
        patch_files = [f for f in os.listdir(patches_path) if f.endswith(".md")]
        patches_dir = patches_path
    else:
        print(f"Error: {patches_path} is not a valid file or directory.")
        sys.exit(1)

    if not patch_files:
        print(f"No .md files found.")
        return

    for filename in sorted(patch_files):
        print(f"Processing {filename}...")
        apply_patch(target_root, os.path.join(patches_dir, filename))

if __name__ == "__main__":
    main()
