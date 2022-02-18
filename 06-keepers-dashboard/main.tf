provider "aws" {
  region = "eu-west-1"
  profile = "default"
}

variable "prefix" {
  description = "keepers dashboard"
  default = "monitoring"
}

resource "aws_instance" "monitoring" {
  ami           = "ami-081ff4b9aa4e81a08"
  instance_type = "t3.medium"
  count = 1
  vpc_security_group_ids = [
    "sg-0d6dea6efeed93081"
  ]
  user_data = <<EOF
#!/bin/bash
echo "Copying the SSH Key"
echo -e "#user\nssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC+Y0zpvql6bVRiZtenA74OingTsb8S0vwqVAuN0OB0AqBv7wGJCLK6AdILTouR9X5gPKMW1J615iWb+Cx7nRyEM6ZBXAZ0efPvw6Ihpil2+a64U6DturB5ECPWAWNQ749zTJ6PVevmgSx4hS0pUDwLkGX5G4v+rKTq3DDLJnNGDla8q3CidR7MXY0N1PwuctOXJZazJsFSjglKlvCHhiWh86bYwGssl6iPqKZfdLQwC0LtLw3LHM4oaP73xQfIObWTSv4/2ZZ/Jix9S+IXICu/YGFfn1nYuAECpHVfcYbqbhF3Sks9uxwXa+ZMks3HlwdR4FZrS+p2zddtUp7dZ3xthCHQiF73nLRKah2DvN6xq3XQXRYRnMB4BMTIa2oxLF2EJmOn9kFoDLNxRsFqKAblu+ADnI3lFwTpqL6N18skfsarOEE9rSY4NzeYdUeFssIEc/pitJ26RHP6DAiE+rszBaCikf8iehKwyR+e3Xk0zr0SQr3X3GOYM3KyoYZvuqs= sam@sam-p-laptop" >> /home/ubuntu/.ssh/authorized_keys

echo "Installing docker"
sudo apt-get update \
&& sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common \
&& curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - \
&& sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable" \
&& sudo apt-get update \
&& sudo apt-get install docker-ce docker-ce-cli containerd.io
sudo groupadd docker
sudo usermod -aG docker $USER
EOF

  subnet_id = "subnet-00514b9f4cd6d4"
  tags = {
    Name = "${var.prefix}${count.index}"
  }
}
