# Linux Simulator

## Overview

The objective is to provide a simple way to simulate a Linux system.

Down the road, it should be an importable library in training projects 
that aim at interacting with a linux system without having to deal with 
the whole overhead of a real system.

The behavior of the simulated system is meant to be entirely controlled
and should be configurable to any extend in order to have scenarios 
built on top of it. For example:

- troubleshooting a high load average caused by too many apache processes,
- troubleshooting a low free disk space caused by too many log files,
- etc.

As a simulator, it is not meant to perform any type of file change or
modification of any real system.

# Roadmap

## Memory

Manipulate memory usage; used / free / buffers / cached / shared

## Disks

Manipulate files in a filesystem, reflecting file size change recursively

## CPU

Manipulate CPU usage; user, system, io, stolen, etc.

## Networking

Manipulate network; including bandwitdh, listening ports, etc

## Processes

Manipulate processes, running, blocked, zombies, mixing with Memory, CPU 
and Networking.

## Clusters

Ability to simulate several systems working in pair; simulating remote
access over SSH, simulate impact from one system against another.

# Long term

Being able to use the same approach for other simulator that could integrate with
this one; like mysql CLI simulator, pgsql, redis, etc. 