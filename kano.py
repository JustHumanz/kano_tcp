import socket,random,time,os,subprocess,select,errno,re
from socket import error as socket_error

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("socket Ok")

s.bind(('0.0.0.0',2525))
s.listen(1)
dir = os.getcwd()+'/img/'

def getRandomFile(path):
    files = os.listdir(path)
    index = random.randrange(0, len(files))
    return files[index]

def ascii(sys,data):
    getimg = getRandomFile(path=dir)
    note = ""
    def command(data):
        if data == "pixel":
            fil = "--pixel"
            return(str(fil))

        elif data == "center":
            fil = "--center"
            return(str(fil))

        elif re.match(r'^(center|pixel) (center|pixel)', data):
            fil = "--center --pixel"
            return(str(fil))

        else:
            fil = ""
            return(str(fil))

    cmd = f'im2a \'{dir}{getimg}\' {command(data)}'
    if "unknown" in getimg:
        note = "if you know the source you can tell me\nTwitter: @Aldin_Py\nEmail: humanz@justhumanz.me"
    else:
        note = "Created by Just_Humanz\nTwitter: @Aldin_Py\nEmail: humanz@justhumanz.me\nIG: aldin0x1101"
    sys = subprocess.check_output(cmd, shell=True).decode('utf-8').rstrip("\n")+f"\nsource: {getimg}\n========================\n{note}"
    return(str(sys))

def sock():
    c, addr = s.accept()
    print("Connection address", addr)
    c.setblocking(0)
    ready = select.select([c], [], [], 0.1)
    if ready[0]:
        data = c.recv(1024)
        try:
            fix = data.decode().rstrip()
            if "help" in fix:
                c.send("\'help\' for show help menu\n\'pixel\' print image in pixel format\n\'center\' print image in center of terminal\n\'pixel center\' mah just like the name".encode())
                c.close()
            else:
                c.send(ascii(sys='',data=fix).encode())
                c.close()
        except Exception as e:
            c.send("WTF you send to me? :(".encode())
            c.close()
    else:
        c.send(ascii(sys='',data='').encode())
    c.close()

while True:
    try:
        sock()
        time.sleep(1)
    except Exception as e:
        print("Error")
        print(e)
        time.sleep(1)
        sock()
