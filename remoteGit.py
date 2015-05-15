import git, os, shutil

DIR_NAME = "temp"
REMOTE_URL = "https://github.com/Dreamland2015/Dreamland.git"

if os.path.isdir(DIR_NAME):
    shutil.rmtree(DIR_NAME)

os.mkdir(DIR_NAME)

repo = git.Repo.init(DIR_NAME)
origin = repo.create_remote('origin', REMOTE_URL)
origin.fetch()
origin.pull(origin.refs[0].remote_head)

print("---- DONE ----")
