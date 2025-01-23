#!/bin/bash

# Change into  relevant directory
cd /home/beth/Desktop/vermicell

# Starting after bothp python interfaces are running.
sleep 70

# Run PureData Patc
puredata -nogui vermicell-pd-patch.pd
 
