module "main" {
  source = "../modules/main"

  env                   = "qa"
  sendgrid_sandbox_mode = "0"
}
