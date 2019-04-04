module "main" {
  source = "../modules/main"

  env                   = "qa"
  instance_type         = "t2.nano"
  sendgrid_sandbox_mode = "0"
}

output "public_ip" {
  value = "${module.main.public_ip}"
}

output "public_domain" {
  value = "${module.main.public_domain}"
}
