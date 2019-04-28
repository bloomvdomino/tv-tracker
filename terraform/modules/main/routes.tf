locals {
  root_domain   = "olivertso.com"
  domain_env    = "${var.env != "production" ? ".${var.env}" : ""}"
  public_domain = "${var.project}${local.domain_env}.${local.root_domain}"
}

data "aws_route53_zone" "root_domain" {
  name = "${local.root_domain}"
}

resource "aws_route53_record" "public_domain" {
  zone_id = "${data.aws_route53_zone.root_domain.zone_id}"
  name    = "${local.public_domain}"
  type    = "A"
  ttl     = "300"
  records = ["${aws_instance.main.public_ip}"]
}
