# -*- coding: utf-8 -*-
import os, random, pathlib
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

# リポジトリ直下を基準に
ROOT = pathlib.Path(__file__).parent
IMAGES = ROOT / "images"
CSV = ROOT / "data.csv"

# 既存のサイト生成スクリプトを呼ぶ
import generate_site  # 同じフォルダにある前提

def ensure_csv_header():
    if not CSV.exists():
        CSV.write_text("date,hex,rgb,caption,image\n", encoding="utf-8")

def today_row_exists(today):
    if not CSV.exists():
        return False
    for line in CSV.read_text(encoding="utf-8").splitlines():
        if line.startswith(today + ","):
            return True
    return False

def hex_to_rgb_ints(hex_code):  # "#AABBCC" -> (170,187,204)
    hex_code = hex_code.lstrip("#")
    return tuple(int(hex_code[i:i+2], 16) for i in (0,2,4))

def make_image(today, hex_str, outfile):
    # 200x200 白背景に160x160の色四角
    image_size, inner_size = 200, 160
    border = (image_size - inner_size) // 2
    r, g, b = [v / 255.0 for v in hex_to_rgb_ints(hex_str)]
    img = np.ones((image_size, image_size, 3))
    img[border:border+inner_size, border:border+inner_size] = (r, g, b)

    plt.imshow(img)
    plt.axis("off")
    plt.text(image_size - 2, image_size - 2, hex_str,
             color="black", fontsize=12, ha="right", va="bottom")
    outfile.parent.mkdir(exist_ok=True, parents=True)
    plt.savefig(outfile, bbox_inches="tight", pad_inches=0.1, dpi=300)
    plt.close()

def append_csv(today, hex_str, rgb_tuple, rel_path):
    # caption はひとまず固定文 ここは後で自由に変えてOK
    line = f"{today},{hex_str},{rgb_tuple[0]} {rgb_tuple[1]} {rgb_tuple[2]},Auto generated color,{rel_path}\n"
    with CSV.open("a", encoding="utf-8") as f:
        f.write(line)

def main():
    ensure_csv_header()
    today = datetime.now().strftime("%Y-%m-%d")

    if today_row_exists(today):
        print(f"already exists for {today} skip generate")
    else:
        # ランダム色を1つ作成
        hex_str = "#{:06x}".format(random.randint(0, 0xFFFFFF)).upper()
        rgb = hex_to_rgb_ints(hex_str)
        rel_path = f"images/{today}.png"
        outfile = ROOT / rel_path
        make_image(today, hex_str, outfile)
        append_csv(today, hex_str, rgb, rel_path)
        print(f"generated {rel_path} {hex_str} {rgb}")

    # サイト全体を再生成
    generate_site.main()
    print("site regenerated")

if __name__ == "__main__":
    main()
