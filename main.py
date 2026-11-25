#!/usr/bin/env python3
"""news-image-20261125: sum up Wednesday 25 November 2026 in one image.

The entry image (entry.png, 1024x1024) was rendered in-session with PIL
and Noto Sans ExtraCondensed (real typography) from the verified 25 Nov
2026 story set; the renderer is news-image-20261125-render.py in the
build notes. This program only copies entry.png to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png). Pure standard
library, no network, deterministic: two runs write the same bytes.
"""
import os
import shutil


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst)


if __name__ == "__main__":
    main()
