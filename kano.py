import socket,random,time,os,subprocess,select

s = socket.socket()
print("socket Ok")

port=2525
s.bind(('0.0.0.0',port))
s.listen(1)

dir = '/home/humanz/py/py_socks/img/'

def getRandomFile(path):
  files = os.listdir(path)
  index = random.randrange(0, len(files))
  return files[index]

def ascii_pixel(sys):
    getimg = getRandomFile(path=dir)
    sys = subprocess.check_output(f'im2a {dir}{getimg} --pixel', shell=True).decode('utf-8').rstrip("\n")+f"\n source: {getimg}\n"
    return(str(sys))

def ascii(sys):
    getimg = getRandomFile(path=dir)
    sys = subprocess.check_output(f'im2a {dir}{getimg}', shell=True).decode('utf-8').rstrip("\n")+f"\n source: {getimg}\n"
    return(str(sys))

def sock():
    c, addr = s.accept()
    print("Connection address", addr)
    c.setblocking(0)
    ready = select.select([c], [], [], 0.1)
    if ready[0]:
        data = c.recv(1024)
        fix = data.decode()
        if "pixel" in fix:
            c.send(ascii_pixel(sys='').encode())
            c.close()
        else:
            c.send(ascii(sys='').encode())
            c.close()
    else:
        c.send(ascii(sys='').encode())
    c.close()

while True:
    sock()
    time.sleep(1)
