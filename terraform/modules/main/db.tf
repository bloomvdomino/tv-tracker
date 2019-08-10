module "db" {
  source = "git@github.com:olivertso/terraform-modules.git//heroku-db"

  project = local.project
  env     = var.env
}
