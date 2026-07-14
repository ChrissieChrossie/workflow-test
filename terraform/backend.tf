terraform {
    backend "s3" {
        bucket = "1407toffee-workflow-terra-bucket"
        key = "terraform.tfstate"
        region = "eu-central-1"
    }
}