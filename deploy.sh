#!/bin/bash -xe
set -Ceux

# setup ssh
mkdir -p -m 700 ~/.ssh
# hide private key
set +x
echo -e "$SSH_PRIVATE_KEY" > ~/.ssh/id_rsa
set -x
chmod 600 ~/.ssh/id_rsa
cat << EOS > ~/.ssh/config
Host *
    StrictHostKeyChecking no
EOS
# update demo server
cat <<EOS | ssh kishikawa@192.168.11.17 bash
set -Ceux
cd ~/gitlab/kishikawa/fastapi
git reset --hard
git fetch origin
git checkout "$CI_COMMIT_SHORT_SHA"
docker-compose stop
docker-compose up -d
EOS
