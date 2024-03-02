variable "credentials" {
  description = "My Credentials"
  default     = "<Path to your Service Account json file>"
  #ex: if you have a directory where this file is called keys with your service account json file
  #saved there as my-creds.json you could use default = "./keys/my-creds.json"
}


variable "project" {
  description = "Project"
  default     = "pelagic-bonbon-387815"
}

variable "region" {
  description = "Region"
  #Update the below to your desired region
  default     = "us-central1"
}

variable "location" {
  description = "Project Location"
  #Update the below to your desired location
  default     = "US"
}


variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  #Update the below to a unique bucket name
  default     = "de_zoomcamp_2024_bucket"
}

variable "gcs_bigquery_name" {
  description = "My BigQuery Dataset Name"
  default = "de_zoomcamp_pj"
}

variable "instance_name" {
  description = "VM instance name"
  default = "vm-01"
}

variable "machine_type" {
  description = "GCP Instance Type"
  default = "e2-medium"
}

variable "zone" {
  description = "Region for GCP instance."
  default     = "us-central1-a"
}
