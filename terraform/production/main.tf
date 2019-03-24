module "main" {
  source = "../modules/main"

  env           = "production"
  instance_type = "t2.micro"

  # Non-secret environment variables.
  allowed_hosts           = "*"
  tmdb_check_wait_seconds = 1800
  default_from_email      = "do-not-respond@tv-tracker.com"
  sendgrid_sandbox_mode   = "False"
}

output "public_dns" {
  value = "${module.main.public_dns}"
}

output "public_ip" {
  value = "${module.main.public_ip}"
}
