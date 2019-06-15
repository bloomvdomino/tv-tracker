locals {
  parameter_store_path = "/${local.project}/${var.env}"
}

data "aws_ssm_parameter" "secret_key" {
  name = "${local.parameter_store_path}/secret_key"
}

data "aws_ssm_parameter" "admin_path" {
  name = "${local.parameter_store_path}/admin_path"
}

data "aws_ssm_parameter" "tmdb_api_key" {
  name = "${local.parameter_store_path}/tmdb_api_key"
}

data "aws_ssm_parameter" "sendgrid_username" {
  name = "${local.parameter_store_path}/sendgrid_username"
}

data "aws_ssm_parameter" "sendgrid_password" {
  name = "${local.parameter_store_path}/sendgrid_password"
}

data "aws_ssm_parameter" "sendgrid_api_key" {
  name = "${local.parameter_store_path}/sendgrid_api_key"
}
