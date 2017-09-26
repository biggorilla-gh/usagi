sudo yum install -y epel-release
sudo yum install -y ansible
sudo yum install -y python-psycopg2

ansible-playbook setup.yaml
