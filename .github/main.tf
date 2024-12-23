provider "google" {
  project = var.projectid
  region  = var.region
}


resource "google_compute_instance" "ce_instance" {
  name                      = var.instance_name
  machine_type              = "e2-custom-6-16384"
  zone                      = var.zone
  allow_stopping_for_update = true

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
      size  = 30
    }
  }

  network_interface {
    network = "default"
    access_config {
      nat_ip = "35.198.242.84"
    }
  }


  metadata = {
    google-logging-enabled = "true"
    startup-script         = <<-EOF
      #!/bin/bash
      sudo apt-get update
      sudo apt-get install ca-certificates curl
      sudo install -m 0755 -d /etc/apt/keyrings
      sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
      sudo chmod a+r /etc/apt/keyrings/docker.asc

      echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
        $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
        sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
      sudo apt-get update
      sudo apt-get -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin unzip
      sudo systemctl enable docker
      sudo systemctl start docker
      sudo sysctl -w vm.max_map_count=262144
    EOF
  }

}

