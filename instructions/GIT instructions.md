# GIT Instructions

Make sure git account is setup in VSCode.  Need to setup username and email.  

Ctrl Shift P: Git clone.  
Set up a directory for git cloning

Move your project folders into the git directory

VSCode will show changes.

## Uploading in Git
 
1. Stage (local machine)
2. Commit (local machine)
3. Sync (sending to git server)

If you run into problems:
Undo Commit, Undo Stage

## setting userid and password

The following is necessary to do the first time, when you try to push to the server, also called sometime "sync"

```
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

<!-- ********************* -->
## Finding out what is your current setting for username and email
<!-- ********************* -->

```
git config --global user.name 
git config --global user.email 
```

<!-- ********************* -->
## First time commit/sync
<!-- ********************* -->

1. Not sure between these two which triggers the credentials challenge
2. When it does, you will be taken to a browser to login once
3. After that it should remember those credentials

<!-- ********************* -->
## How does one work with git in a team
<!-- ********************* -->

1. Very complicated subject
2. And you will get to know as you continue to collaborate

### Mean while, frequently....

1. Frequently...
2. Pull first
3. Make your changes or new files or folders
4. The "source control icon will light up when something new is there

### When ready with your changes

1. Stage (all) files
2. Enter a message and commit
3. Sync (pushing to the server)

<!-- ********************* -->
## What can go wrong with pull
<!-- ********************* -->

1. When you pull...
2. if there are some files that are added/updated, it will give an error
3. So, to resolve, stage them first...
4. If you don't want to stage them (like if they are temporary), copy them somewhere else for now [Bigger topic to understand]
5. Then you should be able to pull the latest
6. Update/change/add
7. stage, commit, and sync