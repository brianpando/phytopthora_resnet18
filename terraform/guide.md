no olvides crear el archivo terraform.tfvars
con los valores que se necesita: 
$ cp terraform.tfvars.example terraform.tfvars

para conseguir el fingerprint de tu pc:
$ ssh-keygen -E md5 -lf ~/.ssh/id_rsa.pub
El fingerprint es la parte despues del MD5, es decir:
2048 MD5:ab:cd:ef:12:34:56:78:90:ab:cd:ef:12:34:56:78:90 user@host => ab:cd:ef:12:34:56:78:90:ab:cd:ef:12:34:56:78:90

o tambien puedes aplicar para generar solo la llave:
$ ssh-keygen -E md5 -lf ~/.ssh/id_rsa.pub | awk '{print $2}' | sed 's/^MD5://'


Para levantar la apliacion en digitalOcean usar:
$ terraform apply
$ terraform destroy


