## About and Prep
This upgrade assumes you installed using either the guide here or provided by CoinCashew as referrenced in this guide. Edit your ~/.bashrc file to include the following two lines if not already there:

export LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH"
export PKG_CONFIG_PATH="/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH"

## Steps to Update

sudo apt-get update -y
sudo apt-get install automake build-essential pkg-config libffi-dev llvm libgmp-dev libssl-dev libtinfo-dev libsystemd-dev zlib1g-dev make g++ tmux git jq wget libncursesw5 libtool autoconf liblmdb-dev -y
sudo apt update
sudo apt upgrade -y

cd ~/git
git clone https://github.com/bitcoin-core/secp256k1.git

cd secp256k1
git reset --hard ac83be33d0956faf6b7f61a60ab524ef7d6a473a
./autogen.sh
./configure --prefix=/usr --enable-module-schnorrsig --enable-experimental
make
make check
sudo make install

ghcup upgrade
ghcup --version

ghcup install ghc 8.10.7
ghcup set ghc 8.10.7
ghc --version

ghcup install cabal 3.6.2.0
ghcup set cabal 3.6.2.0
cabal --version

cd $HOME/git
rm -rf cardano-node-old
git clone https://github.com/input-output-hk/cardano-node.git cardano-node2
cd cardano-node2
cabal update
git fetch --all --recurse-submodules --tags
git checkout $(curl -s https://api.github.com/repos/input-output-hk/cardano-node/releases/latest | jq -r .tag_name)
cabal configure -O0 -w ghc-8.10.7

echo -e "package cardano-crypto-praos\n flags: -external-libsodium-vrf" >> cabal.project.local

cabal build cardano-node cardano-cli

# Backup
cd $HOME/cardano-my-node
mkdir bk_1_34
mv testnet-alonzo-genesis.json bk_1_34/testnet-alonzo-genesis.json
mv testnet-byron-genesis.json bk_1_34/testnet-byron-genesis.json
mv testnet-config.json bk_1_34/testnet-config.json
mv testnet-shelley-genesis.json bk_1_34/testnet-shelley-genesis.json
cp -p testnet-topology.json bk_1_34/testnet-topology.json

sudo cp -p /usr/local/bin/cardano-node cardano-node.1.34.1
sudo cp -p /usr/local/bin/cardano-cli cardano-cli.1.34.1

$(find $HOME/git/cardano-node2/dist-newstyle/build -type f -name "cardano-node") version
$(find $HOME/git/cardano-node2/dist-newstyle/build -type f -name "cardano-cli") version

wget -N https://hydra.iohk.io/job/Cardano/cardano-node/cardano-deployment/latest-finished/download/1/${NODE_CONFIG}-config.json
wget -N https://hydra.iohk.io/job/Cardano/cardano-node/cardano-deployment/latest-finished/download/1/${NODE_CONFIG}-byron-genesis.json
wget -N https://hydra.iohk.io/job/Cardano/cardano-node/cardano-deployment/latest-finished/download/1/${NODE_CONFIG}-shelley-genesis.json
wget -N https://hydra.iohk.io/job/Cardano/cardano-node/cardano-deployment/latest-finished/download/1/${NODE_CONFIG}-alonzo-genesis.json

sudo cp $(find $HOME/git/cardano-node2/dist-newstyle/build -type f -name "cardano-node") /usr/local/bin/cardano-node
sudo cp $(find $HOME/git/cardano-node2/dist-newstyle/build -type f -name "cardano-cli") /usr/local/bin/cardano-cli

cardano-node version
cardano-cli version

# Reboot
