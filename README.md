# Kurator [![CircleCI](https://circleci.com/gh/SaltyCatFish/kurator/tree/master.svg?style=svg)](https://circleci.com/gh/SaltyCatFish/kurator/tree/master)
![](http://saltycatfish.com/wp-content/uploads/2017/10/kurator_worker-e1508625294523.jpg)

Kurator is a project for helping you manage bulk importing media files from a phone, tablet, or any device that you can access via your PC via the shell or command line.

In this version, Kurator has 3 main functions; *import_media, prune, and fix_names*.

## import_media
`Usage: kurator import_media [OPTIONS] SOURCE LIBRARY`
Import media from a source folder to a library (any) folder.  Files will be renamed using their exif metadata if available.  Kurator will group media taken on the same day together, by creating folders for each unique date found in the imported photos.

Folder are created as an 8 digit date - `20171019` would be created for October 19, 2017
Media files are created with a 14 digit timestamp representing the date and time a photo was taken - `20140201-165116.jpg` Would mean the photo was take on February 2, 2014 at 04:51:16 PM.

## prune
`Usage: kurator prune [OPTIONS] TARGET`
Removes duplicate files, comparing the files **contents**, not file names.  Prune will compare each file to every other file in the `TARGET` recursively.  If two or more file contents match, those duplicates are removed from the target.

## fix_names
`Usage: kurator fix_names [OPTIONS] TARGET`
Renames all media files in the `TARGET` directory according to the naming schema in **import_media**.

*Worker with wrench designed by www.slon.pics / Freepik.  Thanks!*


This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* Quick summary
* Version
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### How do I get set up? ###

* Summary of set up
* Configuration
* Dependencies
* Database configuration
* How to run tests
* Deployment instructions

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact

