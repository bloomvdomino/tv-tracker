output "public_dns" {
  value = "${aws_instance.main.public_dns}"
}

output "public_ip" {
  value = "${aws_instance.main.public_ip}"
}
