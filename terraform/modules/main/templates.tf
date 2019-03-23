locals {
  web_env_file_name = "env_file.web"
  db_env_file_name  = "env_file.db"
}

data "template_file" "ec2_init" {
  template = "${file("${path.module}/templates/ec2_init.sh")}"

  vars {
    project            = "${var.project}"
    base_dc_path       = "${local.base_dc_path}"
    production_dc_path = "${local.production_dc_path}"
  }
}

data "template_file" "env_file_web" {
  template = "${file("${path.module}/templates/${local.web_env_file_name}")}"

  vars {
    secret_key        = "${data.aws_ssm_parameter.secret_key.value}"
    admin_path        = "${data.aws_ssm_parameter.admin_path.value}"
    tmdb_api_key      = "${data.aws_ssm_parameter.tmdb_api_key.value}"
    sendgrid_username = "${data.aws_ssm_parameter.sendgrid_username.value}"
    sendgrid_password = "${data.aws_ssm_parameter.sendgrid_password.value}"
    sendgrid_api_key  = "${data.aws_ssm_parameter.sendgrid_api_key.value}"

    env                     = "${var.env}"
    allowed_hosts           = "${var.allowed_hosts}"
    database_url            = "postgres://${var.db_user}:@db:5432/${var.db_name}"
    tmdb_check_wait_seconds = "${var.tmdb_check_wait_seconds}"
    default_from_email      = "${var.default_from_email}"
    sendgrid_sandbox_mode   = "${var.sendgrid_sandbox_mode}"
  }
}

data "template_file" "env_file_db" {
  template = "${file("${path.module}/templates/${local.db_env_file_name}")}"

  vars {
    postgres_db   = "${var.db_name}"
    postgres_user = "${var.db_user}"
  }
}
