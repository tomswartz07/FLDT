# Setup Process

Setup process has been tested for ArchLinux, but should be similar for Ubuntu or other.

ArchLinux was chosen because of the completeness of their documentation with regard to the individual software parts.

## Prerequesites

*Assuming that a base OS install has already been completed:* 
Install the required software as follows:

```bash
# FLDT required
pacman -S nodejs redis cpio git udpcast partclone

# PXE required
pacman -S dnsmasq darkhttpd
```

## Required Files

### Files for FLDT
Make a folder to store the deployable images
```bash
mkdir /images/ # Root folder for all images
mkdir /images/DeployableImageTitle # Folder containing all files needed for DeployableImageTitle's image
```

### Files for Support Services
Now deploy all of the files in the tftpboot.tar.gz archive to the locations defined in the dnsmasq configuration.
```bash
mkdir /pxeboot
cp /path/to/tftpboot.tar.gz /pxeboot
tar xzvf /pxeboot/tftpboot.tar.gz /pxeboot
```

## Services

Next, set up and enable the services.

### dnsmasq
Edit the file /etc/dnsmasq.conf to add the following:
```bash
port=0 # Disables DNS function, only enabling DHCP and TFTP
interface=« ETH INTERFACE » # Replace with Ethernet interface used (eth0, enp2s0, etc)
bind-interfaces
dhcp-range=10.0.0.50,10.0.0.150,45m # Enables DHCP service, 100 devices (ip range 50-150) with expiry of 45 minutes
dhcp-boot=pxelinux.0 # PXE file
dhcp-option-force=209,pxelinux.cfg/default # Defines boot menu options
enable-tftp
tftp-root=/pxeboot # Where all PXE files are stored
```
Finally (re)start the dnsmasq service, and optionally watch the output as devices connect
```bash
ip addr add 10.0.0.1/24 dev «DEVICE NAME» # Start eth device with address for PXE booting
systemctl restart dnsmasq.service
journalctl -u dnsmasq.service -f # Optional
```

### FLDT
Next, set up the FLDT services.
```bash
cd ~/ # We're storing FLDT files in home folder, for ease of location
git clone http://github.com/tomswartz07/FLDT
cd FLDT/server
npm install # Install FLDT service and dependencies
redis-server & # Start Redis server,  '&' will fork it to background
node server.js
```

## Imaging
At this point, most of the heavy work is now complete.

Navigate to http://localhost:8080 to access the FLDT interface

Select the image on the Images page, load the hosts .csv as directed on the Hosts page, and finally enter the number of hosts and begin multicasting on the Multicasting page.

As the targeted devices netboot, they should be picked up by the PXE service.
