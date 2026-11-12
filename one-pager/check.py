"""Print the page count and the left edges and tops of text blocks in a PDF.

Usage: python3 check.py F.pdf
"""
import collections
import re
import subprocess
import sys

pdf = sys.argv[1]
info = subprocess.check_output(["pdfinfo", pdf], text=True)
print("pages:", re.search(r"Pages:\s+(\d+)", info).group(1))

html = subprocess.check_output(["pdftotext", "-bbox-layout", pdf, "-"], text=True)
blocks = re.findall(r'<block xMin="([\d.]+)" yMin="([\d.]+)"', html)
for label, i in (("left edges (x pt: blocks)", 0), ("block tops (y pt: blocks)", 1)):
    print(label)
    for v, n in sorted(collections.Counter(round(float(b[i])) for b in blocks).items()):
        print(f"  {v}: {n}")
