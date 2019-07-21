terraform {
  backend "s3" {
    region  = "us-east-1"
    profile = "tv-tracker-production"
    bucket  = "tv-tracker-terraform"
    key     = "production/terraform.tfstate"
  }
}
