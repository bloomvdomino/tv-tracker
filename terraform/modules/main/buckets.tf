resource "aws_s3_bucket" "main" {
  bucket        = "${var.project}-${var.env}"
  acl           = "private"
  force_destroy = true

  tags = {
    Name      = "${var.project}"
    Env       = "${var.env}"
    Terraform = true
  }
}

resource "aws_s3_bucket_public_access_block" "main" {
  bucket = "${aws_s3_bucket.main.id}"

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
