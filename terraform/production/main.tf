module "main" {
  source = "../modules/main"

  env                   = "production"
  instance_type         = "t2.micro"
  sendgrid_sandbox_mode = "False"
}

output "public_ip" {
  value = "${module.main.public_ip}"
}

output "public_domain" {
  value = "${module.main.public_domain}"
}
