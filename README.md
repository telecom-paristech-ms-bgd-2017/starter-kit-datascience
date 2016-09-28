# Starter Kit Datascience

This repository was created in order to gather work and exercises for the students of the "Kit Datascience" class of Télécom ParisTech's Big Data Mastère Spécialisé.

To add your work to the repository:
 - clone it on your machine 
    - > git clone https://github.com/telecom-paristech-ms-bgd-2017/starter-kit-datascience.git
 - locally, create a folder "firstname-name"
    - > cd starter-kit-datascience && mkdir luke-skywalker && cd luke-skywalker
 - add any files to this folder
    - > touch hello_world.py && echo "print('Hello, world!') > hello_world.py
 - add to index your changes
    - > git add hello_world.py
 - commit your changes
    - > git commit -m "Adding file hello_world.py to my repository"
 - when you are satisfied with your work, pull the changes from the GitHub server, and push yours to the shared repository
    - > git pull
    - > git push

# Without war of pushes (only for advanced user)

To avoid the war of pushes on master branch, create your own branch. You know this issue, you pulled but another user pushed before you just at this moment:

> Of course, you can also make several commits in local, and push rarely to avoid this problem of priority. But create one branch is a good practice.

Create your branch from master:

~~~
$ git checkout -b <firstname>-<lastname>
~~~

Push your branch:

~~~
$ git push --set-upstream origin <firstname>-<lastname>
~~~

Now you can do your normal workflow on your branch (only, see below!): work, git add, git commit, [git pull], git push.

After your work, you can merge your branch into master:

~~~
$ git checkout master && git merge <firstname>-<lastname>
~~~

That is to say, you go to master, then you merge \<firstname\>-\<lastname\>. If you can't go, create a stash see https://git-scm.com/docs/git-stash.

> /!\ Here you merge \<firstname\>-\<lastname\> into master, above all don't merge master into \<firstname\>-\<lastname\>. 
> And if you work directly on web interface of Github, pay attention to be on your branch and don't on master.
> In summary, \<firstname\>-\<lastname\> should be included in master branch, but your branch should be never having
> modifications from master.

Then push master:

~~~
$ git push
~~~

> It is always the war of pushes here, but only for the merge. And the git network graph will more beautiful than before. In addition your commits will be consecutive.

To see your current branch:

~~~
$ git status
~~~

# Without password  

To avoid typing your password for 2 hours without creating a private/public key pair:

~~~
git config --local credential.helper 'cache --timeout 7200'
~~~

You can use --global instead of --local to do that for all of your git repositories, here only for the current repository.




