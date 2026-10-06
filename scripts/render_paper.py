"""Build the review PDF. Requires pandoc, Playwright and Chromium.

Usage: python3 scripts/render_paper.py [--chromium /path/to/chromium]
No publication, upload or repository commit is performed.
"""
import argparse
from pathlib import Path
import shutil
import subprocess
from playwright.sync_api import sync_playwright


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--chromium', default=None)
    args = parser.parse_args()
    paper = Path(__file__).resolve().parents[1] / 'paper'
    subprocess.run(['pandoc', 'manuscript.md', '-s', '--mathjax',
                    '--css=academic.css', '-o', 'manuscript.html'],
                   cwd=paper, check=True)
    executable = args.chromium or shutil.which('chromium') or shutil.which('chromium-browser')
    with sync_playwright() as playwright:
        options = {'headless': True}
        if executable:
            options['executable_path'] = executable
        browser = playwright.chromium.launch(**options)
        try:
            page = browser.new_page()
            page.goto((paper / 'manuscript.html').as_uri(), wait_until='networkidle', timeout=60000)
            page.wait_for_function('window.MathJax && MathJax.startup && MathJax.startup.promise', timeout=60000)
            page.evaluate('async () => { await MathJax.startup.promise; await document.fonts.ready; }')
            errors = page.locator('mjx-merror').count()
            if errors:
                raise RuntimeError(f'MathJax reported {errors} rendering errors')
            if not page.evaluate('Array.from(document.images).every(i => i.complete && i.naturalWidth > 0)'):
                raise RuntimeError('An image failed to load')
            page.pdf(path=str(paper / 'manuscript.pdf'), prefer_css_page_size=True,
                     print_background=True, display_header_footer=False)
        finally:
            browser.close()
    print(f'Rendered {paper / "manuscript.pdf"}')


if __name__ == '__main__':
    main()
