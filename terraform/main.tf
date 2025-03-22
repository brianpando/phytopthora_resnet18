terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

provider "digitalocean" {
  token = var.do_token
}

resource "digitalocean_droplet" "web"{
  name   = "web"
  region = "nyc1"
  size   = "s-1vcpu-2gb"  # 1GB RAM, 1 vCPU
  image  = "ubuntu-22-04-x64"

  ssh_keys = ["c3:97:fe:ce:28:af:32:1c:6f:06:4b:38:f2:79:58:42"]
  
  #user_data = file("${path.module}/install.sh")

  tags = ["flask", "torch", "production"]
}

resource "digitalocean_firewall" "allow_ssh" {
  name = "allow-ssh"

  droplet_ids = [digitalocean_droplet.web.id]

  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }
  inbound_rule {
    protocol         = "tcp"
    port_range       = "5000"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol         = "icmp"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "tcp"
    port_range            = "all"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "udp"
    port_range            = "all"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }
}

output "droplet_ip" {
  value = digitalocean_droplet.web.ipv4_address
}
