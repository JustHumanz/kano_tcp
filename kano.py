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

def ascii(sys,pix):
    getimg = getRandomFile(path=dir)

    def command1(pix):
        if pix == True:
            pix_command = "--pixel"
            return(pix_command)
        else:
            pix_command = ""
            return(pix_command)

    sys = subprocess.check_output(f'im2a {dir}{getimg} {command1(pix)}', shell=True).decode('utf-8').rstrip("\n")+f"\n source: {getimg}\n"
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
                c.send(ascii(sys='',pix= True).encode())
                c.close()
            else:
                c.send(ascii(sys='',pix= False).encode())
                c.close()
        except Exception as e:
            c.send("WTF you send to me? :(".encode())
    else:
        c.send(ascii(sys='',pix= False).encode())
    c.close()

while True:
    try:
        sock()
        time.sleep(1)
    except Exception as e:
        print("Error")
        time.sleep(1)
        sock()
