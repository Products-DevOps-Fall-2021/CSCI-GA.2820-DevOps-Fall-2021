# products

# Setting up the development environment
Install [Git](http://git-scm.com/downloads) for using bash commands.
To setup the development environment, we use [Vagrant](https://www.vagrantup.com/downloads) and [VirtualBox](https://www.virtualbox.org/wiki/Downloads). The recommended code editor is [Visual Studio Code](https://code.visualstudio.com/).

The Vagrantfile installs all of the needed software to run the service. You can clone this github repository and follow the given commands to start running the service:
 
```shell
git clone https://github.com/products-devops-fall-21/products.git  
cd products     
vagrant up
vagrant ssh
cd /vagrant
exit
vagrant halt
```
