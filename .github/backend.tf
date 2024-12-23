terraform {
  backend "gcs" {
    bucket = "transcript-terraform-state"
    prefix = "terraform/state"
  }
}