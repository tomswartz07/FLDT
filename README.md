FLDT
====

The Fast Linux Deployment Toolkit

Developed by Penn Manor High School student Andrew Lobos 
and the Penn Manor IT Team for our 1:1 student laptop program, 
FLDT (Fast Linux Deployment Toolkit) uses a variety of open source 
tools to quickly image and configure either single machines or large
batches of systems. Imaging is accomplished by using partclone to copy and
restore only the used blocks from the file system. Images are able to
be transferred to clients via NFS or multicasted via udpcast. FLDT
also provides methods for running post-image scripts, such as 
machine-specific configurations like automatically
setting hostnames and forcing password change on next boot.
Additionally, the host database and imaging can be managed via a
custom Node.js powered web panel.

References:

Partclone: http://partclone.org/
Udpcast: http://www.udpcast.linux.lu/

Information about the Penn Manor 1:1 student laptop program can be 
found here: http://www.pennmanor.net/techblog/?page_id=1561.

## Install

#### Prerequisites 
* Node.js
* Redis
* A NFS export of /images
* A DHCP server configured for PXE booting, along with TFTPd
* A compiled Linux kernel with support for your hardware, devtmpfs, and NFS filesystems. 

#### Installation
```
# Install Node.js dependencies
cd FLDT/server
npm install
# Build bootimages

cd ../bootimage
./makeimage
cp -r images/* /var/lib/tftpboot
```

Next, setup your PXE infastructure to boot the generated images. If you are unfarmilar with this, you will want to look at the PXELINUX project.

#### Making an image
The default imageing scripts expect these items in an image:
* A folder in /image with the folder's name
* A sfdisk generated partitiontable.txt
* Each partimage image for each partition named with the drive name ( ex The file named sda1 will be restored to /dev/sda1 )

#### Editing for your purposes 
FLDT is not as turn-key as systems like FOG - but it makes up for that in configurability. Each "action" that FLDT can do is a separate script. 
These scripts are put into bootable image. If you need FLDT to do something different, just edit the scripts in bootimage/scripts and run makeimage.sh to regenrate the boot images.

