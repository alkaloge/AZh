#!/bin/bash
if ! test -d "ClosureTest"; then
    mkdir ClosureTest
fi
combineTool.py -M T2W -o "ws.root" -i ClosureTest/all 
for channel in em et mt tt
do 
    if ! test -d "ClosureTest/${channel}"; then
	echo creating folder ClosureTest/${channel}
	mkdir ClosureTest/${channel}
	cp ClosureTest/all/azh_closure_SS_${channel}.root ClosureTest/${channel}
	cp ClosureTest/all/azh_closure_SS_${channel}.txt ClosureTest/${channel}
	combineTool.py -M T2W -o "ws.root" -i ClosureTest/${channel}
    fi
done
