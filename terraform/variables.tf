variable "do_token" {
  description = "Token de acceso a DigitalOcean"
  type        = string
}

variable "ssh_key_fingerprint" {
  description = "Fingerprint de la clave SSH pública en DigitalOcean"
  type        = string
}
