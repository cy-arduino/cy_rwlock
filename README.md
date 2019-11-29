# RwLock: Reader-Writer lock

## Introduction
We can simply protect a shared resource by a lock. But the performance is not
good because each reader should done one-by-one.

A Reader-Writer lock can improve the performance by
1. Let readers running simultaneously
2. Exclude "multiple readers" and each writer

By the way, a writer should wait until all reader done.
In a frequently read situation, a reader after the writer can also increase
the read count, let read count never decrease to 0. This will starve writer.
So RwLock provide a flag "write_first" to block the newer read until the
writer finish it's work.

## Install
1. `pip install cy_rwlock`
1. download from https://pypi.org/project/cy_rwlock/#files


## unittest
- run `scripts\run.bat`


## deploy
- run `scripts\deploy.bat`


## TODO
TBD
