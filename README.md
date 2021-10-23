# products

### Setting up the development environment
Install [Git](http://git-scm.com/downloads) for using bash commands.
To setup the development environment, we use [Vagrant](https://www.vagrantup.com/downloads) and [VirtualBox](https://www.virtualbox.org/wiki/Downloads). The recommended code editor is [Visual Studio Code](https://code.visualstudio.com/).

The Vagrantfile installs all of the needed software to run the service. You can clone this github repository and follow the given commands to start running the service:
 
```bash
git clone https://github.com/products-devops-fall-21/products.git  
cd products     

#bring up the vm
vagrant up 

#open a shell inside the vm
vagrant ssh 

cd /vagrant

cd service

python run.py


#exit out of the vm shell back to your host computer
exit 

#shutdown the vm to return later with vagrant up
vagrant halt 
```


search [127.0.0.1:5000](http://127.0.0.1:5000/) on browser
