locals {
  remote_pwd         = "/home/ubuntu"
  base_dc_path       = "docker/docker-compose.yml"
  production_dc_path = "docker/production/docker-compose.yml"
}

resource "aws_instance" "web" {
  instance_type          = "${var.instance_type}"
  ami                    = "ami-0ac019f4fcb7cb7e6"
  vpc_security_group_ids = ["${aws_security_group.instance.id}"]
  key_name               = "${var.project}"

  connection {
    type        = "ssh"
    user        = "ubuntu"
    private_key = "${file("~/.ssh/aws/${var.project}.pem")}"
  }

  provisioner "remote-exec" {
    inline = [
      "mkdir -p ${local.remote_pwd}/docker/production/",
    ]
  }

  provisioner "file" {
    source      = "../../${local.base_dc_path}"
    destination = "${local.remote_pwd}/${local.base_dc_path}"
  }

  provisioner "file" {
    source      = "../../${local.production_dc_path}"
    destination = "${local.remote_pwd}/${local.production_dc_path}"
  }

  provisioner "file" {
    content     = "${data.template_file.env_file_web.rendered}"
    destination = "${local.remote_pwd}/${local.web_env_file_name}"
  }

  provisioner "file" {
    content     = "${data.template_file.env_file_db.rendered}"
    destination = "${local.remote_pwd}/${local.db_env_file_name}"
  }

  provisioner "remote-exec" {
    inline = <<EOF
${data.template_file.ec2_init.rendered}
EOF
  }

  tags = {
    Name      = "${var.project}"
    Env       = "${var.env}"
    Terraform = true
  }
}
