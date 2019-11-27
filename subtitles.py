import os
import hashlib

lst = [
    {"m":"Is The F-35 Worth $115 Million.mp4","s":"Is The F-35 Worth $115 Million.zh-Hans.ass"}
]

sdir="/Users/yuanliqiang/youtube/"
ddir="/Users/yuanliqiang/tmp/"


def subtitle(item):
    hl = hashlib.md5()
    hl.update(item["m"].encode())
    md5str = hl.hexdigest()

    smpath=sdir+item["m"]
    hmpath=sdir+md5str+".mp4"
    sspath=sdir+item["s"]
    hspath=sdir+md5str+".ass"

    hdpath=ddir+md5str+".mp4"
    dmpath=ddir+item["m"]

    os.rename(smpath,hmpath)
    os.rename(sspath,hspath)
    
    cmd="ffmpeg -y -hwaccel videotoolbox -i {input} -c:v h264_videotoolbox -vf \"ass={subtitle}\" -pix_fmt yuv420p -s hd1080 -b:v 6800K -acodec copy {output};".format(
        input=hmpath,
        subtitle=hspath,
        output=hdpath
    )
    os.system(cmd)

    os.rename(hmpath,smpath)
    os.rename(hspath,sspath)
    os.rename(hdpath,dmpath)

if __name__ == "__main__":
    for item in lst:
        subtitle(item)
