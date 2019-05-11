provider "aws" {
  region  = "us-east-1"
  profile = "${local.project}"
}
