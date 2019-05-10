### IMPORTANT NOTES ###

Once you add a vdev to a pool, you cannot remove it, as the pool immediately sucks up that space and cannot shrink. You can detach a drive from a mirror vdev, destroying the mirror and leaving it as a disk vdev. You can then attach a different drive to that mirror and resilver onto it, then remove the first drive and replace it as well. Once both drives are replaced, you can expand into the new drive space.

https://wiki.ubuntu.com/Kernel/Reference/ZFS
https://blog.fosketts.net/2017/12/11/add-mirror-existing-zfs-drive/
https://linuxhint.com/zfs-concepts-and-tutorial/
https://jrs-s.net/2015/02/06/zfs-you-should-use-mirror-vdevs-not-raidz/

### END NOTES ###

In these examples, vdb and vdc are 5G, and vdd and vde are 10G.

#### create pool

`zpool create <pool-name> <device>`

`zpool create testpool /dev/vdb`



#### attach second device, thus creating a mirror

`zpool attach <pool-name> <existing-device> <new-device>`

`zpool attach testpool /dev/vdb /dev/vdc`



#### add second vdev mirror to existing pool (make sure to use add as this adds more space to the pool)

`zpool add <pool-name> mirror <first-new-device> <second-new-device>`

`zpool add testpool mirror /dev/vdd /dev/vde`

#### end result:

	# zpool status
	  pool: testpool
	 state: ONLINE
	  scan: resilvered 82.5K in 0h0m with 0 errors on Thu May  9 18:03:02 2019
	config:
	
		NAME        STATE     READ WRITE CKSUM
		testpool    ONLINE       0     0     0
		  mirror-0  ONLINE       0     0     0
		    vdb     ONLINE       0     0     0
		    vdc     ONLINE       0     0     0
		  mirror-1  ONLINE       0     0     0
		    vdd     ONLINE       0     0     0
		    vde     ONLINE       0     0     0
	
	errors: No known data errors

	# df -h
	Filesystem      Size  Used Avail Use% Mounted on
	udev            985M     0  985M   0% /dev
	tmpfs           200M  712K  199M   1% /run
	/dev/vda1        20G  1.7G   18G   9% /
	tmpfs           997M     0  997M   0% /dev/shm
	tmpfs           5.0M     0  5.0M   0% /run/lock
	tmpfs           997M     0  997M   0% /sys/fs/cgroup
	/dev/vda15      105M  3.4M  102M   4% /boot/efi
	tmpfs           200M     0  200M   0% /run/user/1000
	testpool         15G  128K   15G   1% /testpool

#### create filesystem

`zfs create <pool-name>/<fs-name>`

`zfs create testpool/one`

	# df -h
	Filesystem      Size  Used Avail Use% Mounted on
	udev            985M     0  985M   0% /dev
	tmpfs           200M  712K  199M   1% /run
	/dev/vda1        20G  1.7G   18G   9% /
	tmpfs           997M     0  997M   0% /dev/shm
	tmpfs           5.0M     0  5.0M   0% /run/lock
	tmpfs           997M     0  997M   0% /sys/fs/cgroup
	/dev/vda15      105M  3.4M  102M   4% /boot/efi
	tmpfs           200M     0  200M   0% /run/user/1000
	testpool         15G     0   15G   0% /testpool
	testpool/one     15G     0   15G   0% /testpool/one

#### filesystem will use all the space available to the pool unless you set a quota

`zfs set quota=<N>G <pool-name>/<fs-name>`

`zfs set quota=2G testpool/one`

	# df -h
	Filesystem      Size  Used Avail Use% Mounted on
	udev            985M     0  985M   0% /dev
	tmpfs           200M  712K  199M   1% /run
	/dev/vda1        20G  1.7G   18G   9% /
	tmpfs           997M     0  997M   0% /dev/shm
	tmpfs           5.0M     0  5.0M   0% /run/lock
	tmpfs           997M     0  997M   0% /sys/fs/cgroup
	/dev/vda15      105M  3.4M  102M   4% /boot/efi
	tmpfs           200M     0  200M   0% /run/user/1000
	testpool         15G     0   15G   0% /testpool
	testpool/one    2.0G  128K  2.0G   1% /testpool/one


#### replacing both drives and expanding into the new bigger drives

`zpool create testpool vdb`  
wait for resilver to finish - verify via zpool status  
`zpool attach testpool vdb vdc`  
wait for resilver to finish - verify via zpool status  
`zpool detach testpool vdb`  
wait for resilver to finish - verify via zpool status  
`zpool attach testpool vdc vdd`  
wait for resilver to finish - verify via zpool status  
`zpool detach testpool vdc`  
wait for resilver to finish - verify via zpool status  
`zpool attach testpool vdd vde`  
wait for resilver to finish - verify via zpool status  
`zpool online -e testpool vdd vde`

	# zpool status
	  pool: testpool
	 state: ONLINE
	  scan: resilvered 120K in 0h0m with 0 errors on Thu May  9 18:19:58 2019
	config:
	
		NAME        STATE     READ WRITE CKSUM
		testpool    ONLINE       0     0     0
		  mirror-0  ONLINE       0     0     0
		    vdd     ONLINE       0     0     0
		    vde     ONLINE       0     0     0
	
	errors: No known data errors
	# df -h
	Filesystem      Size  Used Avail Use% Mounted on
	udev            985M     0  985M   0% /dev
	tmpfs           200M  712K  199M   1% /run
	/dev/vda1        20G  1.7G   18G   9% /
	tmpfs           997M     0  997M   0% /dev/shm
	tmpfs           5.0M     0  5.0M   0% /run/lock
	tmpfs           997M     0  997M   0% /sys/fs/cgroup
	/dev/vda15      105M  3.4M  102M   4% /boot/efi
	tmpfs           200M     0  200M   0% /run/user/1000
	testpool        9.7G     0  9.7G   0% /testpool

#### using autoexpand property - removing the need to use 'online -e'

`zpool create testpool vdb`  
`zpool set autoexpand=on testpool`  

	# zpool list testpool -o autoexpand
	EXPAND
	    on

`zpool attach testpool vdb vdc`  
wait for resilver to finish - verify via zpool status  
`zpool detach testpool vdb`  
wait for resilver to finish - verify via zpool status  
`zpool attach testpool vdc vdd`  
wait for resilver to finish - verify via zpool status  
`zpool detach testpool vdc`  
wait for resilver to finish - verify via zpool status  
`zpool attach testpool vdd vde`  

	# zpool status
	  pool: testpool
	 state: ONLINE
	  scan: resilvered 88.5K in 0h0m with 0 errors on Thu May  9 18:30:30 2019
	config:
	
		NAME        STATE     READ WRITE CKSUM
		testpool    ONLINE       0     0     0
		  mirror-0  ONLINE       0     0     0
		    vdd     ONLINE       0     0     0
		    vde     ONLINE       0     0     0
	
	errors: No known data errors
	# df -h
	Filesystem      Size  Used Avail Use% Mounted on
	udev            985M     0  985M   0% /dev
	tmpfs           200M  712K  199M   1% /run
	/dev/vda1        20G  1.7G   18G   9% /
	tmpfs           997M     0  997M   0% /dev/shm
	tmpfs           5.0M     0  5.0M   0% /run/lock
	tmpfs           997M     0  997M   0% /sys/fs/cgroup
	/dev/vda15      105M  3.4M  102M   4% /boot/efi
	tmpfs           200M     0  200M   0% /run/user/1000
	testpool        9.7G     0  9.7G   0% /testpool



#### creating nfs/samba exports

`apt install nfs-kernel-server`  

Use these sites  
https://vitux.com/install-nfs-server-and-client-on-ubuntu/  
http://www.supermaru.com/2017/05/ubuntu-zfs-samba-share/  
https://help.ubuntu.com/community/How%20to%20Create%20a%20Network%20Share%20Via%20Samba%20Via%20CLI%20%28Command-line%20interface/Linux%20Terminal%29%20-%20Uncomplicated%2C%20Simple%20and%20Brief%20Way%21
