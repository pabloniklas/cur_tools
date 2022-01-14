# VDISK

## Introduction

Long time ago, where DOS was default OS in PC's, the computer ran in "Real Mode", that is, any programm could have
complete access to hardware resources.

Then, when OS/2 appeared in 1993, and with the 80386 CPU from Intel, computers could run in a different mode, called 
"Protected Mode". In this mode any programm had to ask hardware resources to the Kernel. That is how today computers
works.

## VDISK Implementation

Because DOS's debug, ran in real mode, it had access to the whole disk, something that today is not possible. 
That's why I have implemented a virtual disk (vdisk), that can be managed (from PEBUG point of view), as a 
disk in real mode.

## Relevants Commands

* ```w```
* ```n```
* ```l```

