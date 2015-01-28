#-*- coding: utf-8 -*-
#!/usr/bin/env python 
import paramiko
import threading

def ssh2(ip,username,key,cmd):
    try:
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip,22,username,key_filename=key,timeout=5)
        for m in cmd:
            stdin, stdout, stderr = ssh.exec_command(m)
            out = stdout.readlines()
            for o in out:
                print o,
            print '%s\tOK\n'%(ip)
        ssh.close()
    except :
        print '%s\tError\n'%(ip)

if __name__=='__main__':
    cmd = ['cal','echo hello!']
    username = "ec2-user"
    threads = []
    key = '/home/ec2-user/aws_ty.pem'
    print "Begin......"
    for ip in ['54.92.28.215','54.92.67.157', '54.92.91.217']:
        a = threading.Thread(target=ssh2,args=(ip,username,key,cmd))
        a.start()
