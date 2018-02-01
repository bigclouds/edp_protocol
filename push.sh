#!/bin/bash

# tem and hum
#for i in `seq 1 5000`; do  tem=$(( (RANDOM % 50) + 20 ))   ; humm=$(( (RANDOM % 50) + 20 )) ; echo  curl -H \"api-key: tcrgs5KYyd3zIqPZ=7v9QpmwkXM=\" -X POST -d \'\{\"air_tem\":$tem\,\"air_hum\":$humm\}\' "http://api.heclouds.com/devices/24496837/datapoints?type=3" >>a1.sh; done
# light
#curl -H "api-key: 3crqs2KtydSzI6PZ=7v9QpmwkXM=" -X POST -d '{"light_on":1}' "http://api.heclouds.com/devices/24582591/datapoints?type=3"
