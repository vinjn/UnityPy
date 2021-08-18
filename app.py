from __future__ import unicode_literals
import UnityPy
import sys
from io import open
import os
from os import path
from collections import OrderedDict
import multiprocessing

options = {
    'MINIMUM_ASSET_BYTES': 10000
}
def process_asset_folder(asset_folder):
    # all of the following would work
    env = UnityPy.load(asset_folder)
    output_folder = asset_folder + '-pkg'
    os.makedirs(output_folder + '/Texture2D', exist_ok=True)
    os.makedirs(output_folder + '/Font', exist_ok=True)
    os.makedirs(output_folder + '/Shader', exist_ok=True)
    os.makedirs(output_folder + '/Mesh', exist_ok=True)

    for obj in env.objects:
        if obj.byte_size < options['MINIMUM_ASSET_BYTES']:
            continue
        print(obj)
        try:
            # parse the object data
            data = obj.read()
        except Exception:
            print(data.name)
            continue

        if obj.type == "Texture2D":
            if data.m_Width == 0 or data.m_Height == 0:
                continue
            # create destination path
            dest = path.join(output_folder, str(obj.type), data.name)

            # make sure that the extension is correct
            # you probably only want to do so with images/textures
            dest, ext = path.splitext(dest)
            dest = dest + ".png"

            img = data.image
            if img.width > 128 and img.height > 128:
                img.save(dest)
        elif obj.type == "Mesh":
            dest = path.join(output_folder, str(obj.type), data.name + '.obj')
            # with open(dest, "wt", newline = "") as f:
            #     f.write(data.export())
        elif obj.type == "Font":
            if not data.m_FontData: continue
            extension = ".ttf"
            if data.m_FontData[0:4] == b"OTTO":
                extension = ".otf"
            dest = path.join(output_folder, str(obj.type), data.name + extension)
            with open(dest, "wb") as f:
                f.write(data.m_FontData)
        elif obj.type == "Shader":
            name = data.m_ParsedForm.m_Name.replace('/','_')
            dest = path.join(output_folder, str(obj.type), name + '.txt')
            with open(dest, "w", newline = "") as f:
                f.write(data.export())

if __name__ == '__main__':
    global pool
    asset_folder = "../pkg-doctor/_fp0521/base"
    if len(sys.argv) > 1:
        asset_folder = sys.argv[1]
    process_asset_folder(asset_folder)
