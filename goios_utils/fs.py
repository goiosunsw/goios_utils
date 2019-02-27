import os
import psutil

if os.name == 'nt':
    import ctypes
    kernel32 = ctypes.windll.kernel32

    def get_label_w(drive_path):
        buf = ctypes.create_unicode_buffer(1024)
        fsnbuf = ctypes.create_unicode_buffer(1024)
        kernel32.GetVolumeInformationW(ctypes.c_wchar_p(drive_path),
                                       buf, ctypes.sizeof(buf),
                                       fsnbuf, ctypes.sizeof(fsnbuf))
        return buf.value


def find_ext_volume(vol_name):
    """
    Find the path of an external volume based on its label
    """
    for p in psutil.disk_partitions():
        mp = p.mountpoint

        if os.name == 'nt':
            if get_label_w(mp).find(vol_name) > -1:
                return mp
        else:
            if mp.find(vol_name) > -1:
                return mp
