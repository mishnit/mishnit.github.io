# on both instances:
sudo yum install -y amazon-efs-utils
sudo mkdir /efs
sudo mount -t efs fs-yourid:/ /efs

# you can now write files into /efs and they'll be available on both your ec2 instances!
