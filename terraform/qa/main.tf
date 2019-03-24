module "main" {
  source = "../modules/main"

  env           = "qa"
  instance_type = "t2.micro"

  allowed_hosts         = "*"
  default_from_email    = "do-not-respond.qa@tv-tracker.com"
  sendgrid_sandbox_mode = "False"
}

output "public_dns" {
  value = "${module.main.public_dns}"
}

output "public_ip" {
  value = "${module.main.public_ip}"
}
