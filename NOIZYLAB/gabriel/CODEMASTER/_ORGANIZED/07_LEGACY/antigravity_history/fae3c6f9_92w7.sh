#!/bin/bash
echo "FLUSHING PIPES (SUBNET SWEEP)..."
for i in {1..254}; do
    ping -c 1 -W 100 10.0.0.$i > /dev/null 2>&1 &
done
wait
echo "SWEEP COMPLETE."
arp -a
