data "aws_instances" "main" {
  instance_tags = {
    Name      = "${local.infra}"
    Env       = "${var.env}"
    Terraform = true
  }

  instance_state_names = ["running"]
}
