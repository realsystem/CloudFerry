#!/bin/bash

set -e

tenant_name="tenant1"

filter="configs/filter.yaml"
cfg="devlab/config.ini"

src=$(grep grizzly_ip $cfg | awk '{print $3}')
ssh_user=$(grep src_ssh_user $cfg | awk '{print $3}')
ssh_cmd="ssh $ssh_user@${src}"

if [[ $1 == "--tenant" ]]; then
a="awk '{print \$2}'"
tenant_id=$(${ssh_cmd} "keystone tenant-list | grep $tenant_name | $a")
cat <<EOF > $filter
tenants:
    tenant_id:
        - $tenant_id
EOF
fi

