# STATUS builds, xxx need sample & target binary

# XXX theres no binary usable for fuzzing

class libogg:
    name = __name__
    home = "http://xiph.org/ogg/"
    scmOrigin = "git clone https://git.xiph.org/mirrors/ogg.git"
    dataTypes = [
        "ogg"
    ]

    target = "xxx"
    targetParam = "-d"
    aflFuzzParam = ""

    clean = [
        "make distclean"
    ]

    build = [
        "./autogen.sh",
        "CC=afl-gcc ./configure --disable-shared",
        "make"
    ]
