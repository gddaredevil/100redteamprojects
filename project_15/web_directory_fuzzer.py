import threading
import urllib3
import argparse
import queue
import sys

def wordlists(arg):
    with open(arg) as file:
        print("[*] Parsing Wordlist ...   [DONE]")
        wqueue = queue.Queue()
        raw = file.readline()
        while(raw):
            word = raw.strip()
            wqueue.put(word)
            raw = file.readline()
    return wqueue

def bruteforce(wq):
    while not wq.empty():
        word = wq.get()
        ext=['.php','.txt']
        if(args.r):
            if('.' not in word):
                for i in ext:
                    wq.put(word+i)

        if('.' not in word):
            word="/"+str(word)+"/"
        else:
            word="/"+str(word)

        url = "{}{}".format(target,word)

        try:
            http = urllib3.PoolManager()
            head = {}
            head["User-Agent"] = user_agent
            response = http.request("GET", headers=head, url = url)

            if(len(response.data)):
                if(response.status != 404):
                    print("{} => {}".format(response.status, url))
                if(response.status >=200 and response.status<300):
                    if('.' not in url.split('/')[-2] and '.' not in url.split('/')[-1]):
                        uq.put(url)
        except KeyboardInterrupt:
            print("Keyboard Interrupt detected. Quitting ...")
            sys.exit(1)

if __name__ == '__main__':

    uq = queue.Queue()

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"

    parser = argparse.ArgumentParser()
    parser.add_argument("--host")
    parser.add_argument("path")
    parser.add_argument('-r', action='store_true')
    parser.add_argument('-v', action="store_true")
    args = parser.parse_args()

    wordlist = wordlists(args.path)
    host = args.host
    uq.put(host)
    threads=[]

    while not uq.empty():
        target = uq.get()
        if(args.v):
            print("[*] Checking RHOST : {} ...   [DONE]".format(target))
        for i in range(10):
            t = threading.Thread(target=bruteforce, args=(wordlist,))
            threads.append(t)
            t.start()
        for thread in threads:
            thread.join()
