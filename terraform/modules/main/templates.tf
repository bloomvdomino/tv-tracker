locals {
  env_file_web = "env_file.web"
  env_file_db  = "env_file.db"
  db_name      = "tt"
  db_user      = "tt"
}

data "template_file" "instance_init" {
  template = "${file("${path.module}/templates/instance_init.sh")}"

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
    allowed_hosts           = "${local.public_domain}"
    database_url            = "postgres://${local.db_user}:@db:5432/${local.db_name}"
    bucket_name             = "${aws_s3_bucket.main.id}"
    tmdb_check_wait_seconds = "${var.tmdb_check_wait_seconds}"
    default_from_email      = "do-not-respond${local.domain_env}@${var.project}.com"
    sendgrid_sandbox_mode   = "${var.sendgrid_sandbox_mode}"
  }
}

data "template_file" "env_file_db" {
  template = "${file("${path.module}/templates/${local.env_file_db}")}"

  vars {
    postgres_db   = "${local.db_name}"
    postgres_user = "${local.db_user}"
  }
}
