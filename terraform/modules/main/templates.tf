locals {
  env_file_web = "env_file.web"
  env_file_db  = "env_file.db"
  db_name      = "tt"
  db_user      = "tt"
  db_password  = "${data.aws_ssm_parameter.db_password.value}"
}

data "template_file" "ec2_init" {
  template = "${file("${path.module}/templates/ec2_init.sh")}"

  vars {
    project                   = "${var.project}"
    docker_compose_base       = "${local.docker_compose_base}"
    docker_compose_production = "${local.docker_compose_production}"
  }
}

data "template_file" "env_file_web" {
  template = "${file("${path.module}/templates/${local.env_file_web}")}"

  vars {
    secret_key        = "${data.aws_ssm_parameter.secret_key.value}"
    admin_path        = "${data.aws_ssm_parameter.admin_path.value}"
    tmdb_api_key      = "${data.aws_ssm_parameter.tmdb_api_key.value}"
    sendgrid_username = "${data.aws_ssm_parameter.sendgrid_username.value}"
    sendgrid_password = "${data.aws_ssm_parameter.sendgrid_password.value}"
    sendgrid_api_key  = "${data.aws_ssm_parameter.sendgrid_api_key.value}"

    env                     = "${var.env}"
    allowed_hosts           = "${var.allowed_hosts}"
    database_url            = "postgres://${local.db_user}:${local.db_password}@db:5432/${local.db_name}"
    tmdb_check_wait_seconds = "${var.tmdb_check_wait_seconds}"
    default_from_email      = "${var.default_from_email}"
    sendgrid_sandbox_mode   = "${var.sendgrid_sandbox_mode}"
  }
}

data "template_file" "env_file_db" {
  template = "${file("${path.module}/templates/${local.env_file_db}")}"

  vars {
    postgres_db       = "${local.db_name}"
    postgres_user     = "${local.db_user}"
    postgres_password = "${local.db_password}"
  }
}
