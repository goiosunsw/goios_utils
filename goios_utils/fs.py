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
                raise FileNotFoundError
        else:
            if mp.find(vol_name) > -1:
                return mp
            else:
                raise FileNotFoundError


def nist_read(filename):
    import subprocess
    import io
    from scipy.io import wavfile

    proc = subprocess.run(['sph2pipe','-f', 'wav', filename],stdout=subprocess.PIPE)
    riff_chunk_size = len(proc.stdout) - 8
    # Break up the chunk size into four bytes, held in b.
    q = riff_chunk_size
    b = []
    for i in range(4):
        q, r = divmod(q, 256)
        b.append(r)

    # Replace bytes 4:8 in proc.stdout with the actual size of the RIFF chunk.
    riff = proc.stdout[:4] + bytes(b) + proc.stdout[8:]

    #riff=proc.stdout
    sr, w = wavfile.read(io.BytesIO(riff))
