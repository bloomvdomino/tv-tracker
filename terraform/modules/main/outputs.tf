output "public_ip" {
  value = "${aws_instance.main.public_ip}"
}

output "public_domain" {
  value = "${aws_route53_record.public_domain.name}"
}
