import git


def PullRepo():
	g = git.cmd.Git('/Users/geethree/Documents/Repo/Dreamland')
	g.pull()
