## Cardano Node Upgrade Steps and Scripts + Vasil PreProd Instructions

Steps for upgrading to latest Cardano node and cli, based on the "Coincashew" configuration.

### Scriptable Steps:
##### Update system
```
sudo apt update
sudo apt upgrade -y
```

##### Install libsecp256k1 (if not previously installed)
```
cd $HOME/git
git clone https://github.com/bitcoin-core/secp256k1
cd secp256k1
git checkout ac83be33
./autogen.sh
./configure --enable-module-schnorrsig --enable-experimental
make
make check
sudo make install
sudo ldconfig
```

##### Backup existing node build/binaries
```
mkdir $HOME/cardano-my-node/old_node
sudo cp /usr/local/bin/cardano-cli $HOME/cardano-my-node/old_node/cardano-cli
sudo cp /usr/local/bin/cardano-node $HOME/cardano-my-node/old_node/cardano-node
mv $HOME/git/cardano-node $HOME/cardano-my-node/old_node/cardano-node
```

##### Install Cabal
```
cd $HOME
ghcup upgrade
ghcup install cabal 3.6.2.0
ghcup set cabal 3.6.2.0
```

##### Install GHC
```
ghcup install ghc 8.10.7
ghcup set ghc 8.10.7
```

##### Update Cabal and verify versions
##### IMPORTANT: Cabal should be at version 3.6.2.0 and GHC should be at version 8.10.7
```
cabal update
cabal --version
ghc --version
```

##### Build the latest node and cli binaries
```
cd $HOME/git
git clone https://github.com/input-output-hk/cardano-node.git
cd cardano-node
git fetch --all --recurse-submodules --tags
git checkout $(curl -s https://api.github.com/repos/input-output-hk/cardano-node/releases/latest | jq -r .tag_name)
cabal configure -O0 -w ghc-8.10.7
echo -e "package cardano-crypto-praos\n flags: -external-libsodium-vrf" > cabal.project.local
sed -i $HOME/.cabal/config -e "s/overwrite-policy:/overwrite-policy: always/g"
rm -rf $HOME/git/cardano-node/dist-newstyle/build/x86_64-linux/ghc-8.10.7
cabal build cardano-cli cardano-node
```

##### This build process will take a while

##### Stop Node and Replace Cardano Binaries
```
sudo systemctl stop cardano-node
sudo cp $(find $HOME/git/cardano-node/dist-newstyle/build -type f -name "cardano-cli") /usr/local/bin/cardano-cli
sudo cp $(find $HOME/git/cardano-node/dist-newstyle/build -type f -name "cardano-node") /usr/local/bin/cardano-node
```

##### Verify versions are up to date/expected versions
```
cardano-node version
cardano-cli version
```

##### Restart Node Into New Version
```
sudo systemctl start cardano-node
```

### Using Minted on Testnet
With the latest changes in the testnet surrounding the Vasil hardfork, there are now several available testnets. For testing Minted we recommend utilizing the PreProd network. To utilize preprod, your testnet full node will need a few pieces in place, the following checklist relates directly to a "Coincashew setup" however can be used in many different node setup configurations.

- In your `~/cardano-my-node/env` file, update these lines:
```
CONFIG="${NODE_HOME}/config.json"
SOCKET="${NODE_HOME}/db-preprod/socket"
```
- In your `~/.bashrc` file, find and update the following 2 lines, using your home folder path:
```
export TESTNET_MAGIC_NUM=1
```
```
export CARDANO_NODE_SOCKET_PATH=/home/user/cardano-my-node/db-preprod/socket
```
- Download the tar file found in this repository containing the PreProd config files and extract them into your `~/cardano-my-node` directory.
- In your `~/cardano-my-node/startCardanoNode.sh` file, find and update the following lines:
...
```
TOPOLOGY=\${DIRECTORY}/topology.json
DB_PATH=\${DIRECTORY}/db-preprod
SOCKET_PATH=\${DIRECTORY}/db-preprod/socket
CONFIG=\${DIRECTORY}/config.json
```
...

After you make the above changes to your system, reboot or manually export the new system variables for them to take effect in your terminal, and you will be able to begin using the new PreProd network!
