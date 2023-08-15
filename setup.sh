#! /bin/zsh
pkill -9 -f iannix2TUIO.py
pkill -9 -f leap2TUIO.py
open -a iannix src/scores/cylinder-follow.iannix &
sleep 1
open -a max src/server.maxpat &
sleep 1
/Applications/Pd.app/Contents/MacOS/Pd src/processor.pd &
sleep 1
python3 src/iannix2TUIO.py &
sleep 1
python3 src/leap2TUIO.py &
echo done
