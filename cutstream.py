#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import hashlib
import re
import os
import json

bdir = "/Users/yuanliqiang/workspace/youtube-dl/"
sdir = "/Users/yuanliqiang/youtube/"
ddir = "/Users/yuanliqiang/tmp/"
lx = 1350
ly = 1010
logo = "/Users/yuanliqiang/workspace/youtube-dl/mengmadianjing.png"
proxy = "socks5://127.0.0.1:1081"
display = {}


def gettitle(url):
    # test proxy connection
    cmd = "{bin}youtube-dl -F --no-check-certificate --proxy {proxy} \"{url}\"".format(
        bin=bdir,
        url=url,
        proxy=proxy
    )
    print(cmd)
    os.system(cmd)
    # get title
    shell = "{bin}youtube-dl -f 'best' --buffer-size 16k --retries infinite --no-check-certificate --proxy {proxy} --get-title \"{url}\"".format(
        bin=bdir,
        proxy=proxy,
        url=url
    )
    print(shell)
    p = subprocess.Popen(shell, shell=True, stdout=subprocess.PIPE)
    out, err = p.communicate()
    return out.strip().decode('utf-8')


def download(url):
    title = re.sub(r'[\\\/\:\*\?\"\'\<\>\|\.]', "", gettitle(url))
    hl = hashlib.md5()
    hl.update(title.encode())
    md5str = hl.hexdigest()

    spath = sdir+md5str+".mp4"
    dpath = ddir+md5str+".mp4"

    # download vc
    shell = [
        "{bin}youtube-dl -f '(bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4])' --buffer-size 16k --write-thumbnail --retries infinite --no-check-certificate".format(
            bin=bdir
        )]

    shell.append("--proxy {proxy} \"{url}\" -o '{spath}'".format(
        proxy=proxy,
        url=url,
        spath=spath
    ))
    print(shell)
    os.system(" ".join(shell))

    cmd = "ffmpeg -y -hwaccel videotoolbox -threads 4 -i {spath} -c:v h264_videotoolbox -vf \"movie={logo}[watermark];[in][watermark]overlay={lx}:{ly}\" -pix_fmt yuv420p -s hd1080 -b:v 6800K -acodec copy {dpath}".format(
        spath=spath,
        logo=logo,
        lx=lx,
        ly=ly,
        dpath=dpath
    )
    os.system(cmd)
    os.rename(dpath, ddir+title+".mp4")


if __name__ == "__main__":
    with open("/Users/yuanliqiang/workspace/youtube-dl/lst","r") as f:
        for line in f.readlines():
            download(line)
