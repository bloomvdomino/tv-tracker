variable "env" {}

variable "project" {
  default = "tv-tracker"
}

variable "instance_type" {}

variable "allowed_hosts" {}

variable "tmdb_check_wait_seconds" {
  default = 1800
}

variable "default_from_email" {}

variable "sendgrid_sandbox_mode" {}
