# How to run?

## Server (not replicated)
### In zookeeper bin directory:
bash zkServer.sh start-foreground

## Server (replicated)
### 1. Create config files in separate directories
1.1 Files should be named *zoo.cfg*
1.2 Files shoud contain:

dataDir=*path_to_myid_file (for example: /tmp/zookeeper/zk1)*
clientPort=*for example: 2182*
server.1=*address_ip_or_host_name (for example: localhost)*:2888:3888
server.2=*address_ip_or_host_name (for example: localhost)*:2889:3889
server.3=*address_ip_or_host_name (for example: localhost)*:2890:3890

### 2. Create *myid* files in directories specified in config files
### 3. In zookeeper bin directory:
bash zkServer.sh --config *relative_or_absolute_path_to_config_directory (for example: ./../conf/c1)* start-foreground

## Client
### In zookeeper bin directory:
bash zkCli.sh -server *address_and_port (for example: 127.0.0.1:2181)*

## App (ZooFollower)
### In this directory:
python ./main.py


# How to use?
## Initial steps
### 1. Type host *address:port* (for example *127.0.0.1:2181*)
### 2. Type external app command to run when ZNode */a* will be created (for example *gedit* or *wireshark*)

## App commands
### 1. tree
This command returns a zookeeper tree of */a* ZNode
### 2. x
This command terminates the program.
### 3. *Ctrl + C*
This action also terminates the program.