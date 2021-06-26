#!/bin/bash
echo "generating van_path"
echo ${1}
cd data_points
./generator ${1} && ./hotspot_kmc < data && ./ant_routing < hotspots
echo "van_path generated"