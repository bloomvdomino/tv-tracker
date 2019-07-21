data "aws_vpc" "default" {
  default = true
  state   = "available"
}

data "aws_instances" "main" {
  instance_tags = {
    Name      = "${local.infra}"
    Env       = "${var.env}"
    Terraform = true
  }

  instance_state_names = ["running"]
}

data "template_file" "container_definitions" {
  template = "${file("${path.module}/templates/container_definitions.json")}"

  vars {
    env                     = "${var.env}"
    allowed_hosts           = "${local.domain}, ${data.aws_instances.main.private_ips.0}"
    database_backup_dir     = "${local.project}/db_backups/"
    bucket_name             = "${local.infra}-${var.env}"
    tmdb_check_wait_seconds = "${var.tmdb_check_wait_seconds}"
    default_from_email      = "do-not-respond${local.domain_env}@${local.project}.com"
    sendgrid_sandbox_mode   = "${var.sendgrid_sandbox_mode}"

    secret_key_arn        = "${data.aws_ssm_parameter.secret_key.arn}"
    admins_arn            = "${data.aws_ssm_parameter.admins.arn}"
    admin_path_arn        = "${data.aws_ssm_parameter.admin_path.arn}"
    database_url_arn      = "${aws_ssm_parameter.database_url.arn}"
    tmdb_api_key_arn      = "${data.aws_ssm_parameter.tmdb_api_key.arn}"
    sendgrid_username_arn = "${data.aws_ssm_parameter.sendgrid_username.arn}"
    sendgrid_password_arn = "${data.aws_ssm_parameter.sendgrid_password.arn}"
    sendgrid_api_key_arn  = "${data.aws_ssm_parameter.sendgrid_api_key.arn}"
  }
}

module "aws_ecs_app" {
  source = "git@github.com:olivertso/terraform-modules.git//aws-ecs-app"

  infra   = "${local.infra}"
  project = "${local.project}"
  env     = "${var.env}"

  vpc_id      = "${data.aws_vpc.default.id}"
  hosted_zone = "${local.hosted_zone}"

  container_definitions = "${data.template_file.container_definitions.rendered}"
  container_name        = "web"
  container_port        = 8000

  health_check_path = "/popular_shows/"
}
