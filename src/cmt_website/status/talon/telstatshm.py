from attr import define, field

# defining format strings for C structs
now = "9d8s"

motorinfo = "c13i10di"

telaxes = "3i8d"

objany = "2Bc4f2d2fhB"

objss = f"{objany}4f"

objpl = f"{objss}i"
objf = f"{objany}2c2B3f"
obje = f"{objss}7f2dfi"
objh = f"{2d8f}"
objp = f"{objss}2d7f"
objes = f"{objany}2d7fi5fi"
obj = f"{objany}{objss}{objpl}{objf}{obje}{objh}{objp}{objp}{objes}"
scan = f"32s32s128s80s80s80s{obj}4d5idic4ic"

wxstats = "2i4s3i3d2i"

telstatshm_struct = f"@{now}i20d{motorinfo}{telaxes}5ic4i2d2i{scan}{wxstats}"
