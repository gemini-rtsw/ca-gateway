#!/bin/bash

# evaluate hostname and set TCS IP depending on the beginning
# (simulation or production env, depending on site and sbf/hbf or mko/cpo)
source "$(dirname $0)/../../etc/tcs-ip.conf"

HBF=$(hostname |egrep '^hbf')
SBF=$(hostname |egrep '^sbf')
MKO=$(hostname |egrep '^mko')
CPO=$(hostname |egrep '^cpo')

if [ "$HBF" != "" ]; then
  TCS_IP=$HBF_TCS_IP
elif [ "$SBF" != "" ]; then
  TCS_IP=$SBF_TCS_IP
elif [ "$MKO" != "" ]; then
  TCS_IP=$MKO_TCS_IP
elif [ "$CPO" != "" ]; then
  TCS_IP=$CPO_TCS_IP
  GEN_IP=$CPO_GEN_IP
  AG_IP=$CPO_AG_IP
else
  TCS_IP=$DEFAULT_IP
fi

$(dirname $0)/../../bin/linux-x86_64/gateway -pvlist /gem_conf/rt/cagateway/GATEWAY.pvlist \
                      -access /gem_conf/rt/cagateway/GATEWAY.access \
                      -log /var/log/ca-gateway/gengateway.log \
                      -prefix gengate -archive -no_cache -debug 1 \
                      -cip "${GEN_IP}" -report /var/log/ca-gateway/gengateway.txt &

$(dirname $0)/../../bin/linux-x86_64/gateway -pvlist /gem_conf/rt/cagateway/GATEWAY-TCS.pvlist \
                      -access /gem_conf/rt/cagateway/GATEWAY.access \
                      -log /var/log/ca-gateway/tcsgateway.log \
                      -prefix tcssgate -archive -no_cache -debug 1 \
                      -cip "${TCS_IP}" -report /var/log/ca-gateway/tcsgateway.txt &

$(dirname $0)/../../bin/linux-x86_64/gateway -pvlist /gem_conf/rt/cagateway/GATEWAY-AG.pvlist \
                      -access /gem_conf/rt/cagateway/GATEWAY.access \
                      -log /var/log/ca-gateway/AGgateway.log \
                      -prefix aggate -archive -no_cache -debug 1 \
                      -cip "${AG_IP}" -report /var/log/ca-gateway/aggateway.txt &

