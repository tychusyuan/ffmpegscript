import os
import hashlib

lst = [
    "HIGHLIGHTS - EVOLUTION OF BOSTON DYNAMICS 2012-2019.mp4"
]

sdir="/Users/yuanliqiang/youtube/"
ddir="/Users/yuanliqiang/tmp/"
lx=1300
ly=900
rx=1860
ry=1060

def subtitle(f):
    hl = hashlib.md5()
    hl.update(f.encode())
    md5str = hl.hexdigest()

    smpath=sdir+f
    hmpath=sdir+md5str+".mp4"

    hdpath=ddir+md5str+".mp4"
    dmpath=ddir+f

    os.rename(smpath,hmpath)
    
    cmd="ffmpeg -y -hwaccel videotoolbox -i {input} -c:v h264_videotoolbox -vf \"delogo=x={lx}:y={ly}:w={w}:h={h}\" -pix_fmt yuv420p -s hd1080 -b:v 6800K -acodec copy {output};".format(
        input=hmpath,
        lx=lx,
        ly=ly,
        w=rx-lx,
        h=ry-ly,
        output=hdpath
    )
    os.system(cmd)

    os.rename(hmpath,smpath)
    os.rename(hdpath,dmpath)

if __name__ == "__main__":
    for item in lst:
        subtitle(item)
