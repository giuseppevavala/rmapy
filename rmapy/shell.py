import json
from lib2to3.pytree import Base
import re
from typing import List
from rmapy.api import Client
from rmapy.blob import DIRECTORY, DOCUMENT, Blob, Tree


class Cmd:
    def __init__(self, name, func, reg, help) -> None:
        self.func = func
        self.help = help
        self.reg = re.compile(reg)


class Shell:
    def __init__(self, tree: Tree, client: Client) -> None:
        self.WORKING_BLOB: Blob = None
        self.blobs = tree.root_blobls
        self.cmds: List[Cmd] = command_list
        self.client = Client
        self._refresh_work_dir()

    def _refresh_work_dir(self):
        self.directorys = list(
            filter(lambda x: x.type == DIRECTORY, self.blobs))
        self.files = list(filter(lambda x: x.type == DOCUMENT, self.blobs))

    def start_shell(self):
        while True:
            user_input = input("> ")
            for cmd in self.cmds:
                res = cmd.reg.match(user_input)
                if res != None:
                    try:
                        cmd.func(self, *res.groups())
                    except BaseException as ex:
                        print("Error: ", ex)


command_list = []


def ls_cmd(shell: Shell):
    count = 0
    for shell.blob in shell.directorys:
        print(f"{count} - {shell.blob.metadata['visibleName']}/")
        count += 1
    for shell.blob in shell.files:
        print(f"{count} - {shell.blob.metadata['visibleName']}")
        count += 1


def cd_cmd(shell: Shell, arg: str):
    if arg == "..":
        if shell.WORKING_BLOB != None:
            shell.WORKING_BLOB = shell.WORKING_BLOB.parent
    else:
        try:
            dir_num = int(arg)
            shell.WORKING_BLOB = shell.directorys[dir_num]
        except (ValueError, IndexError):
            raise Exception("You need to insert valid directory")

    shell.blobs = shell.WORKING_BLOB.childs
    shell._refresh_work_dir()


def metadata_cmd(shell: Shell, arg: str):
    try:
        blob_num = int(arg)
        if (blob_num <= len(shell.directorys)):
            blob = shell.directorys[blob_num]
        else:
            file_num = int(arg) - len(shell.directorys)
            blob = shell.files[file_num]
        print(json.dumps(blob.metadata, indent=4, sort_keys=True))
    except:
        raise Exception("You need to insert a number: metadata <num>")


command_list.append(Cmd("ls", ls_cmd,              "^ls$",
                    "ls - list file/directory in current dir"))
command_list.append(Cmd("cd", cd_cmd,              "^cd\s(.*)$",
                    "cd <num> | .. - change current dir"))
command_list.append(Cmd("metadata", metadata_cmd,  "^metadata\s(.*)$",
                    "metadata <num> - print metadata of blob"))
