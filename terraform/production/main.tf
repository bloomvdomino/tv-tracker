module "main" {
  source = "../modules/main"

  env                   = "production"
  sendgrid_sandbox_mode = "0"
}
