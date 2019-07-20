module "main" {
  source = "../modules/main"

  env                   = "qa"
  vpc_id                = "${var.vpc_id}"
  sendgrid_sandbox_mode = "0"
}
