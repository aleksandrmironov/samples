Playbook run howto

Requirements:
    1)User/group sqoop exists at target system
    2)Mysql jdbc driver downloaded and available at $mysql_jdbc_local_path$
     
Run: ansible-playbook -u ansible -s -i '192.168.1.23,' playbook.yml
