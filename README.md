[![Coverage](https://codecov.io/gh/cy-arduino/cy_rwlock/branch/master/graph/badge.svg)](https://codecov.io/gh/cy-arduino/cy_rwlock)


# RwLock: Reader-Writer lock

## Release Note
1. V1.2: 
    1. fix version convert issue in setup.py
1. V1.1: 
    1. Reduce test time
    1. Refactoring
1. V1.0: first release

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

## Usage

### Install
1. `pip install cy_rwlock`
1. download latest version from https://pypi.org/project/cy_rwlock/#files

#### Example
1. Reader
    1. <pre>from rwlock import RwLock</pre>
    1. <pre>rwlock = RwLock()</pre>
    1. <pre>
        rwlock.acquire_r()
        //Do read
        rwlock.release_r()
        </pre>
    1. OR
    1. <pre>
        with rwlock.lock_r():
            //Do read
        </pre>
1. Writer
    1. <pre>from rwlock import RwLock</pre>
    1. <pre>rwlock = RwLock()</pre>
    1. <pre>
        rwlock.acquire_w()
        //Do write
        rwlock.release_w()
        </pre>
    1. OR
    1. <pre>
        with rwlock.lock_w():
            //Do write
        </pre>
    
1. full example:
    1. https://github.com/cy-arduino/cy_rwlock/blob/master/rwlock/tests/test_rwlock.py

### Unittest
* run `scripts\run.bat`

### Deploy
- run `scripts\deploy.bat`

