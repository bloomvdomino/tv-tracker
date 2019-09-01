locals {
  project              = "tv-tracker"
  app_name             = "${local.project}-olivertso${var.env == "production" ? "" : "-${var.env}"}"
  parameter_store_path = "/${local.project}/${var.env}"
}

variable "env" {
  type = string
}

variable "tmdb_check_wait_seconds" {
  type    = number
  default = 1800
}

variable "sendgrid_sandbox_mode" {
  type    = string
  default = "1"
}
