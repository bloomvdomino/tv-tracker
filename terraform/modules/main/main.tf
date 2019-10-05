data "aws_ssm_parameter" "admin_path" {
  name = "${local.parameter_store_path}/admin_path"
}

data "aws_ssm_parameter" "tmdb_api_key" {
  name = "${local.parameter_store_path}/tmdb_api_key"
}

resource "random_string" "secret_key" {
  length = 64
}

resource "heroku_app" "default" {
  name   = local.app_name
  region = "us"
  stack  = "container"

  config_vars = {
    ALLOWED_HOSTS      = "${local.app_name}.herokuapp.com"
    DEFAULT_FROM_EMAIL = "noreply@${local.project}${local.env_suffix}.com"
    ENV                = var.env
  }

  sensitive_config_vars = {
    SECRET_KEY = random_string.secret_key.result

    ADMIN_PATH   = data.aws_ssm_parameter.admin_path.value
    TMDB_API_KEY = data.aws_ssm_parameter.tmdb_api_key.value
  }
}

resource "heroku_addon" "db" {
  app  = heroku_app.default.name
  plan = "heroku-postgresql:hobby-dev"
}

resource "heroku_addon" "logdna" {
  app  = heroku_app.default.name
  plan = "logdna:quaco"
}

resource "heroku_addon" "scheduler" {
  app  = heroku_app.default.name
  plan = "scheduler:standard"
}

resource "heroku_addon" "sendgrid" {
  app  = heroku_app.default.name
  plan = "sendgrid:starter"
}

resource "heroku_addon" "sentry" {
  app  = heroku_app.default.name
  plan = "sentry:f1"
}
