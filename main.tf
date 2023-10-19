variable "gh_user" {
  description = "Name of GitHub user to access the url"
  type        = string
}

locals {
  repo_url = "https://github.com/${var.gh_user}/dnd-explorer-experiment.git"
}

variable "key_name" {
  description = "Name of key for AWS access"
  type        = string
}

provider "aws" {
  region = "eu-west-2"
}

# Existing variables and configurations ...

resource "aws_msk_cluster" "monster_cluster" {
  cluster_name           = "monster-cluster-1"
  kafka_version          = "2.8.1"
  number_of_broker_nodes = 3
  
  broker_node_group_info {
    instance_type   = "kafka.t3.small"
    ebs_volume_size = 100
    client_subnets = [
      "subnet-a41657de", 
      "subnet-7213161b", 
      "subnet-3c118570"
    ]
    security_groups = ["sg-39d6e247"]
  }

  encryption_info {
    encryption_at_rest_kms_key_arn = "arn:aws:kms:eu-west-2:404544469985:key/33a39a70-daa6-4f13-a5d1-6e198a96cd4c"
    encryption_in_transit {
      client_broker = "PLAINTEXT"
      in_cluster    = true
    }
  }

  client_authentication {
    unauthenticated = true
  }

  open_monitoring {
    prometheus {
      jmx_exporter {
        enabled_in_broker = false
      }
      node_exporter {
        enabled_in_broker = false
      }
    }
  }
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
              git clone ${local.repo_url} /home/ec2-user/dnd-explorer-experiment
              EOF


  tags = {
    Name = "MakersMonsterEC2"
  }

    
  
}

output "instance_public_ip" {
  value = aws_instance.msk_client.public_ip
}
