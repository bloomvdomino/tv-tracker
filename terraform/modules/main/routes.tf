data "aws_route53_zone" "root_domain" {
  name = "${local.root_domain}"
}

resource "aws_route53_record" "public_domain" {
  zone_id = "${data.aws_route53_zone.root_domain.zone_id}"
  name    = "${local.public_domain}"
  type    = "A"
  ttl     = "300"
  records = ["${data.aws_instances.main.public_ips.0}"]
}
