terraform {
  backend "s3" {
    region  = "us-east-1"
    profile = "tv-tracker"
    bucket  = "tv-tracker-terraform"
    key     = "qa/terraform.tfstate"
  }
}
