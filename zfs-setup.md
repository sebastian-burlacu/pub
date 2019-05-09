### IMPORTANT NOTES ###

Once you add a vdev to a pool, you cannot remove it, as the pool immediately sucks up that space and cannot shrink. You can detach a drive from a mirror vdev, destroying the mirror and leaving it as a disk vdev. You can then attach a different drive to that mirror and resilver onto it, then remove the first drive and replace it as well.

### END NOTES ###

#### create pool

`zpool create <pool-name> <device>`

`zpool create testpool /dev/vdb`



#### attach second device

`zpool attach <pool-name> <existing-device> <new-device>`

`zpool attach testpool /dev/vdb /dev/vdc`



#### add second vdev mirror to existing pool

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



