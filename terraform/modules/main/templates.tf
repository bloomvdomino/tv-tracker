locals {
  db_name = "tt"
  db_user = "tt"
}

data "template_file" "app_init" {
  template = "${file("${path.module}/templates/app_init.sh")}"

  vars {
    project                   = "${local.project}"
    docker_compose_base       = "${local.docker_compose_base}"
    docker_compose_production = "${local.docker_compose_production}"
  }
}

data "template_file" "env_file_web" {
  template = "${file("${path.module}/templates/env_file.web")}"

  vars {
    secret_key        = "${data.aws_ssm_parameter.secret_key.value}"
    admins            = "${data.aws_ssm_parameter.admins.value}"
    admin_path        = "${data.aws_ssm_parameter.admin_path.value}"
    tmdb_api_key      = "${data.aws_ssm_parameter.tmdb_api_key.value}"
    sendgrid_username = "${data.aws_ssm_parameter.sendgrid_username.value}"
    sendgrid_password = "${data.aws_ssm_parameter.sendgrid_password.value}"
    sendgrid_api_key  = "${data.aws_ssm_parameter.sendgrid_api_key.value}"

    env                     = "${var.env}"
    virtual_host            = "${local.public_domain}"
    allowed_hosts           = "${local.public_domain}"
    database_url            = "postgres://${local.db_user}:@db:5432/${local.db_name}"
    database_backup_dir     = "${local.project}/db_backups/"
    bucket_name             = "${local.infra}-${var.env}"
    tmdb_check_wait_seconds = "${var.tmdb_check_wait_seconds}"
    default_from_email      = "do-not-respond${local.domain_env}@${local.project}.com"
    sendgrid_sandbox_mode   = "${var.sendgrid_sandbox_mode}"
  }
}

data "template_file" "env_file_db" {
  template = "${file("${path.module}/templates/env_file.db")}"

  vars {
    postgres_db   = "${local.db_name}"
    postgres_user = "${local.db_user}"
  }
}
