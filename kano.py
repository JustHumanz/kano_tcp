import socket,random,time,os,subprocess,select,errno
from socket import error as socket_error

s = socket.socket()
print("socket Ok")

s.bind(('0.0.0.0',2525))
s.listen(1)
dir = os.getcwd()+'/img/'

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
        try:
            fix = data.decode()
            if "pixel" in fix:
                c.send(ascii_pixel(sys='').encode())
                c.close()
            else:
                c.send(ascii(sys='').encode())
                c.close()
        except Exception as e:
            c.send("WTF you send to me? :(".encode())
    else:
        c.send(ascii(sys='').encode())
    c.close()

while True:
    try:
        sock()
        time.sleep(1)
    except Exception as e:
        print("Error")
        time.sleep(1)
        sock()
