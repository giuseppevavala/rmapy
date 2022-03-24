from logging import INFO, getLogger, StreamHandler, Formatter
from rmapy.api import Client
from rmapy.blob import Blob, DOCUMENT, DIRECTORY
import json

# https://my.remarkable.com/device/desktop/connect


log = getLogger("rmapy")
log.setLevel(INFO)

ch = StreamHandler()
ch.setLevel(INFO)

formatter = Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

log.addHandler(ch)
rmapy = Client()

rmapy.is_auth()
rmapy.renew_token()
# rmapy.refresh_tree()
tree = rmapy.reload_tree_cache()

WORKING_BLOB: Blob = None
blobs = tree.root_blobls
directorys = []
files = []

while True:
    cmd = input("> ")
    if cmd == "ls":
        directorys = list(filter(lambda x: x.type == DIRECTORY, blobs))
        files = list(filter(lambda x: x.type == DOCUMENT, blobs))

        count = 0
        for blob in directorys:
            print(f"{count} - {blob.metadata['visibleName']}/")
            count += 1
        for blob in files:
            print(f"{count} - {blob.metadata['visibleName']}")
            count += 1

    elif cmd == "cd ..":
        if WORKING_BLOB != None:
            WORKING_BLOB = WORKING_BLOB.parent
            blobs = WORKING_BLOB.childs
    elif cmd.startswith("cd "):
        dir_num = int(cmd[2:])
        WORKING_BLOB = directorys[dir_num]
        blobs = WORKING_BLOB.childs
    elif cmd.startswith("info "):
        file_num = int(cmd[5:]) - len(directorys)
        print (file_num)
        print (files[file_num].metadata)
