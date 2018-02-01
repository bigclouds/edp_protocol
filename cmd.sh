#edp cmd
curl -H "Content-Type: application/json" -H "api-key: coSivwr8sEk0Hnt154IgMWdqVqk=" -X POST  "api.heclouds.com/cmds?device_id=24613664&qos=1&type=0" -d 'open=1'
curl -X GET  -H "api-key: coSivwr8sEk0Hnt154IgMWdqVqk=" api.heclouds.com/cmds/3d777864-7776-5194-900d-a0e337fa0339
curl -X GET  -H "api-key: coSivwr8sEk0Hnt154IgMWdqVqk=" api.heclouds.com/cmds/3d777864-7776-5194-900d-a0e337fa0339/resp

# tem and hum
for i in `seq 1 5000`; do  tem=$(( (RANDOM % 50) + 20 ))   ; humm=$(( (RANDOM % 50) + 20 )) ; echo  curl -H \"api-key: rcrqs2KYydSzIqPZ=7v9QpmwkXM=\" -X POST -d \'\{\"air_tem\":$tem\,\"air_hum\":$humm\}\' "http://api.heclouds.com/devices/24496837/datapoints?type=3" >>a1.sh; done
# light
curl -H "api-key: rcrqs2KYydSzIqPZ=7v9QpmwkXM=" -X POST -d '{"light_on":1}' "http://api.heclouds.com/devices/24582590/datapoints?type=3"
