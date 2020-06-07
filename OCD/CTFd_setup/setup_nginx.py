import sys

def main(hostname,cert,key):
    with open('OCD/ssl_cert/nginx.conf','r') as f:
        nginxfile = f.read() 
        nginxfile = nginxfile % (hostname,hostname,hostname,cert,key)

    with open('CTFd/conf/nginx/nginx.conf','w') as f:
        f.write(nginxfile)

if __name__ == '__main__':
    main(sys.argv[1],sys.argv[2],sys.argv[3])
