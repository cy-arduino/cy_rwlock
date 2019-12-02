# RwLock: Reader-Writer lock

## Introduction
We can simply protect a shared resource by a lock. But the performance is not
good because each reader should run one-by-one.

A Reader-Writer lock can improve the performance by let readers running 
simultaneously.

By the way, a writer should wait until all readers done.
In a frequently read situation, a new reader after the writer can also increase
the read count, let read count never decrease to 0. 
This will starve writer.

RwLock:
1. Let readers running simultaneously.
1. Exclude "multiple readers" and each writer.
1. provide a flag "write_first" to prevent starve writer.

## Install
1. `pip install cy_rwlock`
1. download from https://pypi.org/project/cy_rwlock/#files


## unittest
- run `scripts\run.bat`


## deploy
- run `scripts\deploy.bat`


## TODO
* autogen pypi project description
