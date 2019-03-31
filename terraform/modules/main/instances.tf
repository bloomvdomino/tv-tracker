locals {
  remote_pwd                = "/home/ubuntu"
  docker_compose_base       = "docker/docker-compose.yml"
  docker_compose_production = "docker/production/docker-compose.yml"
}

resource "aws_instance" "main" {
  instance_type          = "${var.instance_type}"
  ami                    = "ami-0ac019f4fcb7cb7e6"
  vpc_security_group_ids = ["${aws_security_group.instance.id}"]
  iam_instance_profile   = "${aws_iam_instance_profile.main.name}"
  key_name               = "${var.project}"

  tags = {
    Name      = "${var.project}"
    Env       = "${var.env}"
    Terraform = true
  }
}

resource "null_resource" "provisioners" {
  triggers {
    docker_compose_base       = "${file("../../${local.docker_compose_base}")}"
    docker_compose_production = "${file("../../${local.docker_compose_production}")}"
    env_file_web              = "${data.template_file.env_file_web.rendered}"
    env_file_db               = "${data.template_file.env_file_db.rendered}"
    instance_init             = "${data.template_file.instance_init.rendered}"
  }

  connection {
    type        = "ssh"
    user        = "ubuntu"
    private_key = "${file("~/.ssh/aws/${var.project}.pem")}"
    host        = "${aws_instance.main.public_ip}"
  }

  provisioner "remote-exec" {
    inline = [
      "mkdir -p ${local.remote_pwd}/docker/production/",
    ]
  }

  provisioner "file" {
    source      = "../../${local.docker_compose_base}"
    destination = "${local.remote_pwd}/${local.docker_compose_base}"
  }

  provisioner "file" {
    source      = "../../${local.docker_compose_production}"
    destination = "${local.remote_pwd}/${local.docker_compose_production}"
  }

  provisioner "file" {
    content     = "${data.template_file.env_file_web.rendered}"
    destination = "${local.remote_pwd}/${local.env_file_web}"
  }

  provisioner "file" {
    content     = "${data.template_file.env_file_db.rendered}"
    destination = "${local.remote_pwd}/${local.env_file_db}"
  }

  provisioner "remote-exec" {
    inline = <<EOF
${data.template_file.instance_init.rendered}
EOF
  }
}
