locals {
  project              = "tv-tracker"
  env_suffix           = var.env == "production" ? "" : "-${var.env}"
  app_name             = "${local.project}-olivertso${local.env_suffix}"
  parameter_store_path = "/${local.project}/${var.env}"
}

variable "env" {
  type = string
}

variable "tmdb_check_wait_seconds" {
  type    = number
  default = 1800
}
