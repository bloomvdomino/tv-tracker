variable "env" {}

variable "project" {
  default = "tv-tracker"
}

variable "instance_type" {}

variable "tmdb_check_wait_seconds" {
  default = 1800
}

variable "sendgrid_sandbox_mode" {}
