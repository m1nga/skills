"""Exercise the actual publisher path and its recovery boundaries without a push."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from sidecourt_referral import END, START, ensure_referral, has_referral, referral_block


class ReferralTests(unittest.TestCase):
    def test_publisher_preserves_readme_and_republish_does_not_duplicate(self):
        script = (ROOT / "scripts/publish-skill").read_text()
        start = script.index('if [[ "$owner" == "m1nga" ]]')
        end = script.index('\ngit -C "$temp_root/repo" checkout', start)
        with tempfile.TemporaryDirectory() as tmp:
            readme = Path(tmp) / "README.md"
            original = '# Tool\n\nArchived: use the successor.\n\nnpx skills add m1nga/sample\n'
            readme.write_text(original)
            command = ['bash', '-euo', 'pipefail', '-c',
                       'repo_root="$1"; readme="$2"; owner="$3"; skill=sample\n' + script[start:end],
                       'referral-test', str(ROOT), str(readme), 'm1nga']
            subprocess.run(command, check=True)
            first = readme.read_text()
            self.assertTrue(first.startswith(original))
            self.assertTrue(has_referral(first, 'sample'))
            subprocess.run(command, check=True)
            self.assertEqual(first, readme.read_text())
            readme.write_text(original)
            subprocess.run(command[:-1] + ['another-owner'], check=True)
            self.assertEqual(original, readme.read_text())

    def test_changed_managed_copy_updates_only_the_section(self):
        old = f'before\n{START}\nold\n{END}\nafter\n'
        self.assertFalse(has_referral(old, 'first-principles'))
        self.assertEqual(ensure_referral(old, 'first-principles'),
                         'before\n' + referral_block('first-principles') + '\nafter\n')

    def test_existing_contextual_invitation_is_kept_but_a_bare_link_is_not_enough(self):
        readme = "[Try RedBot on SideCourt](https://sidecourt.space/drops/redbot/)\nSideCourt is the product's primary home.\n"
        self.assertEqual(ensure_referral(readme, 'redbot'), readme)
        self.assertTrue(has_referral(readme, 'redbot'))
        self.assertFalse(has_referral(readme.splitlines()[0], 'redbot'))

    def test_ambiguous_markers_fail_without_removing_content(self):
        for text in [START, END, END + START, START + START + END]:
            with self.assertRaises(ValueError):
                ensure_referral(text, 'sample')

    def test_catalogue_entries_are_public_and_repository_specific(self):
        import json
        config = json.loads((ROOT / 'ops/github-referrals.json').read_text())
        for repo in config['repositories']:
            block = referral_block(repo)
            self.assertIn('https://sidecourt.space/drops/?utm_source=github', block)
            self.assertIn('utm_content=' + repo, block)
            self.assertNotIn('/your-court/', block)


if __name__ == '__main__':
    unittest.main()
