from logging import INFO, DEBUG, getLogger, StreamHandler, Formatter
from rmapy.api import Client
from rmapy.shell import Shell

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

rmapy.upload_file("/home/giuseppe/Scrivania/test.epub", "funziona_epub")
rmapy.upload_file("/home/giuseppe/Scrivania/ref_12986035.pdf", "funziona_pdf")

#rmapy.refresh_tree()
# tree = rmapy.reload_tree_cache()

# shell = Shell(tree, rmapy)
# shell.start_shell()