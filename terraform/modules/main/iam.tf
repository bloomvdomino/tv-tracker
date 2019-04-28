data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    actions = [
      "sts:AssumeRole",
    ]

    principals {
      type = "Service"

      identifiers = [
        "ec2.amazonaws.com",
      ]
    }
  }
}

resource "aws_iam_role" "assume_role" {
  name               = "${var.project}-${var.env}"
  assume_role_policy = "${data.aws_iam_policy_document.assume_role.json}"

  tags = {
    Name      = "${var.project}"
    Env       = "${var.env}"
    Terraform = true
  }
}

data "aws_iam_policy_document" "main" {
  statement {
    effect = "Allow"

    actions = [
      "s3:GetObject",
      "s3:ListBucket",
      "s3:PutObject",
    ]

    resources = [
      "${aws_s3_bucket.main.arn}",
      "${aws_s3_bucket.main.arn}/*",
    ]
  }
}

resource "aws_iam_role_policy" "main" {
  name   = "${var.project}-${var.env}"
  role   = "${aws_iam_role.assume_role.id}"
  policy = "${data.aws_iam_policy_document.main.json}"
}

resource "aws_iam_instance_profile" "main" {
  name = "${var.project}-${var.env}"
  role = "${aws_iam_role.assume_role.name}"
}
