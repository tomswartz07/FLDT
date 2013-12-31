FLDT
====

The Fast Linux Deployment Toolkit

Developed by student Penn Manor High School student Andrew Lobos 
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
