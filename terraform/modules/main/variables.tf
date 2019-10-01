locals {
  project              = "tv-tracker"
  env_suffix           = var.env == "production" ? "" : "-${var.env}"
  app_name             = "${local.project}-olivertso${local.env_suffix}"
  parameter_store_path = "/${local.project}/${var.env}"
}

variable "env" {
  type = string
}
