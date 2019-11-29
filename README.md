# Polling Hub

## Introduction
Handle multiple polling task in a single polling hub.
Default execute each callback synchronously.

## Install
1. `pip install pollinghub`
1. download from https://pypi.org/project/pollinghub/#files


## Usage
- see `examples/example.py`


## unittest
- run `scripts\test.bat`


## deploy
- run `scripts\deploy.bat`


## TODO
- warning if some callback run too long
- Support asynchronous callback.
  - run in other thread/process?
  - use thread/process pool?
  - if run asynchronously, user should use a THREAD-SAFE callback!
- ~~Add unit test.~~
- add name for polling_hub
