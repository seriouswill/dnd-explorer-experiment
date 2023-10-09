variable "repo_url" {
  description = "The URL of the git repository to clone"
  type        = string
  default     = "https://github.com/your-default-repo.git"  # Optional default value
}

variable "key_name" {
  description = "Name of key for AWS access"
  type        = string
}

provider "aws" {
  region = "eu-west-2"
}

resource "aws_instance" "msk_client" {
  ami             = "ami-0b2287cff5d6be10f" # Amazon Linux 2 AMI (HVM) - Kernel 5.10, SSD Volume Type
  instance_type   = "t2.small"
  vpc_security_group_ids = ["sg-097cc69c4394149d2"] # Use the existing security group ID
  key_name        = "${var.key_name}" # Ensure you have this key pair in AWS
  user_data = <<-EOF
              #!/bin/bash
              sudo yum update -y
              sudo yum install -y python3
              sudo yum install -y java-1.8.0-openjdk-devel
              sudo yum install -y git
              
              # Install confluent-kafka for Python
              pip3 install --user confluent-kafka

             
              

              # Clone the git repository
              git clone ${var.repo_url} /home/ec2-user/
              EOF


  tags = {
    Name = "WillsMonsterEC2"
  }

    
  
}

output "instance_public_ip" {
  value = aws_instance.msk_client.public_ip
}
