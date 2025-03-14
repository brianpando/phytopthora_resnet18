provider "digitalocean" {
  token = var.do_token
}

resource "digitalocean_droplet" "flask_server" {
  name   = "cacao-flask-app"
  region = "nyc3"
  size   = "s-1vcpu-1gb"  # 1GB RAM, 1 vCPU
  image  = "ubuntu-22-04-x64"

  ssh_keys = var.ssh_keys

  user_data = file("${path.module}/install.sh")

  tags = ["flask", "torch", "production"]
}

output "droplet_ip" {
  value = digitalocean_droplet.flask_server.ipv4_address
}
