import os
import unittest
import shutil
import tempfile
from apply_patches import apply_patch

class TestApplyPatches(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.smali_dir = os.path.join(self.test_dir, "smali/X")
        os.makedirs(self.smali_dir)
        self.patch_dir = os.path.join(self.test_dir, "patches")
        os.makedirs(self.patch_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_basic_replacement(self):
        smali_path = os.path.join(self.smali_dir, "test.smali")
        with open(smali_path, 'w') as f:
            f.write('.method public test()V\n    const-string v0, "old"\n    return-void\n.end method')

        patch_path = os.path.join(self.patch_dir, "patch.md")
        with open(patch_path, 'w') as f:
            f.write('# Patch\n\n## File: `smali/X/test.smali`\n\n### Search for:\n```smali\n    const-string v0, "old"\n```\n\n### Replace with:\n```smali\n    const-string v0, "new"\n```')

        apply_patch(self.test_dir, patch_path)

        with open(smali_path, 'r') as f:
            content = f.read()
        self.assertIn('"new"', content)
        self.assertNotIn('"old"', content)

    def test_append(self):
        smali_path = os.path.join(self.smali_dir, "test.smali")
        with open(smali_path, 'w') as f:
            f.write('.class Ltest;')

        patch_path = os.path.join(self.patch_dir, "patch.md")
        with open(patch_path, 'w') as f:
            f.write('# Patch\n\n## File: `smali/X/test.smali`\n\n### Append to file:\n```smali\n.method public new()V\n    return-void\n.end method\n```')

        apply_patch(self.test_dir, patch_path)

        with open(smali_path, 'r') as f:
            content = f.read()
        self.assertIn(".method public new()V", content)

    def test_multiple_files_in_one_patch(self):
        smali1 = os.path.join(self.smali_dir, "t1.smali")
        smali2 = os.path.join(self.smali_dir, "t2.smali")
        with open(smali1, 'w') as f: f.write("A")
        with open(smali2, 'w') as f: f.write("B")

        patch_path = os.path.join(self.patch_dir, "multi.md")
        with open(patch_path, 'w') as f:
            f.write('## File: `smali/X/t1.smali`\n### Search for:\n```smali\nA\n```\n### Replace with:\n```smali\nC\n```\n\n**File:** `smali/X/t2.smali`\n### Search for:\n```smali\nB\n```\n### Replace with:\n```smali\nD\n```')

        apply_patch(self.test_dir, patch_path)

        with open(smali1, 'r') as f: self.assertEqual(f.read(), "C")
        with open(smali2, 'r') as f: self.assertEqual(f.read(), "D")

    def test_normalization(self):
        smali_path = os.path.join(self.smali_dir, "test.smali")
        with open(smali_path, 'wb') as f:
            f.write(b'line1\r\nline2')

        patch_path = os.path.join(self.patch_dir, "patch.md")
        with open(patch_path, 'w') as f:
            f.write('## File: `smali/X/test.smali`\n### Search for:\n```smali\nline1\nline2\n```\n### Replace with:\n```smali\nwin\n```')

        apply_patch(self.test_dir, patch_path)

        with open(smali_path, 'r') as f:
            self.assertEqual(f.read(), "win")

if __name__ == "__main__":
    unittest.main()
