locals {
  app_dir     = "/apps/${local.project}"
  app_dir_tmp = "/home/ubuntu/${local.project}_tmp"

  docker_compose_base       = "docker/docker-compose.yml"
  docker_compose_production = "docker/production/docker-compose.yml"
}

resource "null_resource" "provisioner" {
  triggers {
    docker_compose_base       = "${file("../../${local.docker_compose_base}")}"
    docker_compose_production = "${file("../../${local.docker_compose_production}")}"
    env_file_web              = "${data.template_file.env_file_web.rendered}"
    env_file_db               = "${data.template_file.env_file_db.rendered}"
    app_init                  = "${data.template_file.app_init.rendered}"
  }

  connection {
    type        = "ssh"
    user        = "ubuntu"
    private_key = "${file("~/.ssh/aws/${local.infra}.pem")}"
    host        = "${data.aws_instances.main.public_ips.0}"
  }

  provisioner "remote-exec" {
    inline = [
      "mkdir -p ${local.app_dir_tmp}/docker/production/",
    ]
  }

  provisioner "file" {
    source      = "../../${local.docker_compose_base}"
    destination = "${local.app_dir_tmp}/${local.docker_compose_base}"
  }

  provisioner "file" {
    source      = "../../${local.docker_compose_production}"
    destination = "${local.app_dir_tmp}/${local.docker_compose_production}"
  }

  provisioner "file" {
    content     = "${data.template_file.env_file_web.rendered}"
    destination = "${local.app_dir_tmp}/docker/env_file.web"
  }

  provisioner "file" {
    content     = "${data.template_file.env_file_db.rendered}"
    destination = "${local.app_dir_tmp}/docker/env_file.db"
  }

  provisioner "file" {
    content     = "${data.template_file.app_init.rendered}"
    destination = "${local.app_dir_tmp}/app_init.sh"
  }

  provisioner "remote-exec" {
    inline = [
      "sudo rm -rf ${local.app_dir}",
      "sudo mv ${local.app_dir_tmp} ${local.app_dir}",
      "cd ${local.app_dir}",
      "sh app_init.sh",
    ]
  }
}
