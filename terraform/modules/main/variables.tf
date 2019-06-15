locals {
  infra         = "hobby-infra"
  project       = "tv-tracker"
  root_domain   = "olivertso.com"
  domain_env    = "${var.env != "production" ? ".${var.env}" : ""}"
  public_domain = "${local.project}${local.domain_env}.${local.root_domain}"
}

variable "env" {}

variable "tmdb_check_wait_seconds" {
  default = 1800
}

variable "sendgrid_sandbox_mode" {
  default = "1"
}
