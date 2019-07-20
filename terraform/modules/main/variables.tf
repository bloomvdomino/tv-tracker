locals {
  infra   = "hobby-infra"
  project = "tv-tracker"

  hosted_zone = "olivertso.com"
  domain_env  = "${var.env != "production" ? ".${var.env}" : ""}"
  domain      = "${local.project}${local.domain_env}.${local.hosted_zone}"

  parameter_store_path = "/${local.project}/${var.env}"
}

variable "env" {}

variable "vpc_id" {}

variable "tmdb_check_wait_seconds" {
  default = 1800
}

variable "sendgrid_sandbox_mode" {
  default = "1"
}
