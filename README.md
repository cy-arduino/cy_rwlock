
[![Python Version](https://img.shields.io/pypi/pyversions/cy_rwlock.svg)](https://pypi.org/project/cy-rwlock/)
[![Pypi Version](https://img.shields.io/pypi/v/cy_rwlock.svg)](https://pypi.org/project/cy-rwlock/)
[![Code size in bytes](https://img.shields.io/github/languages/code-size/cy-arduino/cy_rwlock.svg)](https://pypi.org/project/cy-rwlock/#files)


[![Coverage](https://codecov.io/gh/cy-arduino/cy_rwlock/branch/master/graph/badge.svg)](https://codecov.io/gh/cy-arduino/cy_rwlock)


[![License](https://img.shields.io/pypi/l/cy_rwlock.svg)](https://github.com/cy-arduino/cy_rwlock/blob/master/LICENSE)



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

After 1.6.0, RwLock can support multi-thread(default) and multi-process.
For multi-process scenario, use `rwlock = RwLock(cross_process=True)`

## Usage

### Install
1. `pip install cy_rwlock`
1. download latest version from https://pypi.org/project/cy_rwlock/#files

#### Example
<pre><code>
from rwlock import RwLock

rwlock = RwLock()

### READER
rwlock.acquire_r()
# read...
rwlock.release_r()

# OR
with rwlock.lock_r():
    # read...

### WRITER
rwlock.acquire_w()
# write...
rwlock.release_w()

# OR
with rwlock.lock_w():
    # write...
</code></pre>

### Unittest
* local(windows)
    * run `scripts\run.bat`
* github
    * auto run when push

### Deploy
* PyPI version
    * convertd from git tag
        * see [setup.py](https://github.com/cy-arduino/cy_rwlock/blob/master/setup.py): convert_version()
* local(windows)
    * run `scripts\deploy.bat`
* github -> PyPI
    * When release in github

### Version control
* cy-rwlock XX.YY.ZZ
    * XX.YY match the latest git tag.
    * ZZ will increase automatically when new commit appear in master branch.
    * XX: Update when change architecture
    * YY: Update when add or modify some features
    * ZZ: Update when bugfix or minor changes.
